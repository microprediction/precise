"""Conditional covariance by composition: estimate volatilities and correlation separately.

DCC's ``H = D R D`` decomposition is really a *composition pattern*, not one algorithm. This
generalizes it: plug in any **per-series volatility model** for ``D`` and any **correlation
estimator** for ``R`` (run on the standardized residuals), and recombine.

* The volatility model can be any positional estimator from this package used in 1-D (an estimator
  on a single series *is* a variance tracker), or any ``microprediction/skaters`` univariate model
  via :func:`from_skater`. precise does not depend on ``skaters`` — the adapter is duck-typed.
* The correlation estimator can be any positional estimator from this package; its ``correlation_``
  is used as ``R``.

``DCCCovariance(r)`` is essentially the special case
``ConditionalCovariance(EwaCovariance(r), EwaCovariance(r))``. Now you can say "robust per-series
vol + shrunk correlation", "a skaters Holt model + factor correlation", and so on — a combinatorial
family from two axes.

Standardization is honest one-step-ahead: each observation is standardized by the forecast made
*before* it was seen, then the volatility models are advanced.
"""

from __future__ import annotations

import numpy as np

from precise._conventions import as_rows
from precise.base import BaseOnlineCovariance
from precise.ewa import EwaCovariance


def _clone(est: BaseOnlineCovariance) -> BaseOnlineCovariance:
    return type(est)(**est.get_params())


class _PreciseVar:
    """Adapt a positional estimator used in 1-D as a univariate volatility model."""

    def __init__(self, est: BaseOnlineCovariance):
        self._est = est

    def push(self, y: float) -> None:
        self._est.partial_fit(np.array([y], dtype=float))

    @property
    def mean(self) -> float:
        return float(self._est.location_[0]) if self._est.n_samples_ > 0 else 0.0

    @property
    def variance(self) -> float:
        return float(self._est.covariance_[0, 0]) if self._est.n_samples_ > 0 else 1.0


class _SkaterVar:
    """Adapt a microprediction/skaters callable ``f(y, state) -> (dists, state)``.

    Uses the one-step-ahead forecast ``dists[0]``: ``.mean`` and ``.std`` give the predictive
    mean and standard deviation of the next observation.
    """

    def __init__(self, f):
        self._f = f
        self._state = None
        self._mean = 0.0
        self._var = 1.0

    def push(self, y: float) -> None:
        dists, self._state = self._f(float(y), self._state)
        d0 = dists[0]
        self._mean = float(d0.mean)
        self._var = float(d0.std) ** 2

    @property
    def mean(self) -> float:
        return self._mean

    @property
    def variance(self) -> float:
        return self._var


class _SkaterVarFactory:
    """A picklable zero-argument factory that builds a fresh :class:`_SkaterVar` per series."""

    def __init__(self, f):
        self.f = f

    def __call__(self) -> _SkaterVar:
        return _SkaterVar(self.f)


def from_skater(f) -> _SkaterVarFactory:
    """Adapt a ``microprediction/skaters`` callable into a volatility-model factory.

    ``f`` is a skater: ``f(y, state) -> (list[Dist], state)`` with ``Dist.mean`` / ``Dist.std``.
    Returns a zero-argument factory suitable as the ``vol`` argument of
    :class:`ConditionalCovariance`::

        import skaters
        from precise import ConditionalCovariance, LedoitWolfCovariance, from_skater
        est = ConditionalCovariance(vol=from_skater(skaters.holt),
                                    corr=LedoitWolfCovariance(r=0.05))

    (The factory is picklable when ``f`` is; precise's own estimators are picklable as volatility
    models out of the box.)
    """
    return _SkaterVarFactory(f)


class ConditionalCovariance(BaseOnlineCovariance):
    """Covariance composed from a per-series volatility model and a correlation estimator.

    :param vol:   A positional estimator instance (used in 1-D, cloned per series) or a
                  :func:`from_skater` factory. Default :class:`~precise.ewa.EwaCovariance`.
    :param corr:  A positional estimator instance whose ``correlation_`` is used as ``R``.
                  Default :class:`~precise.ewa.EwaCovariance`.
    """

    def __init__(self, vol=None, corr=None):
        self.vol = vol if vol is not None else EwaCovariance()
        self.corr = corr if corr is not None else EwaCovariance()
        super().__init__()
        self._vol_models: list | None = None
        self._corr_model: BaseOnlineCovariance | None = None

    def _make_vol(self):
        v = self.vol
        if isinstance(v, BaseOnlineCovariance):
            return _PreciseVar(_clone(v))
        if callable(v):
            return v()
        raise TypeError("vol must be a positional estimator instance or a from_skater(...) factory")

    def partial_fit(self, X, y=None) -> ConditionalCovariance:
        for x in as_rows(X):
            if self._state is None:
                d = len(x)
                self.n_features_in_ = d
                self._vol_models = [self._make_vol() for _ in range(d)]
                self._corr_model = _clone(self.corr)
                self._state = {"n_dim": d, "n_samples": 0, "mean": np.zeros(d), "var": np.ones(d)}
            models = self._vol_models
            assert models is not None and self._corr_model is not None
            # One-step-ahead standardization: use the forecast made before seeing x.
            m = np.array([vm.mean for vm in models])
            v = np.array([max(vm.variance, 1e-12) for vm in models])
            eps = (x - m) / np.sqrt(v)
            self._corr_model.partial_fit(eps)
            for i, vm in enumerate(models):
                vm.push(float(x[i]))
            self._state["mean"] = np.array([vm.mean for vm in models])
            self._state["var"] = np.array([max(vm.variance, 1e-12) for vm in models])
            self._state["n_samples"] += 1
        return self

    def _state_to_cov(self, state: dict) -> np.ndarray:
        assert self._corr_model is not None
        R = self._corr_model.correlation_
        d = np.sqrt(np.maximum(np.asarray(state["var"], dtype=float), 1e-12))
        return R * np.outer(d, d)  # H = D R D

    # State is composed of sub-model objects, so the plain-dict JSON serialization of the base
    # estimators does not apply; use pickle (__getstate__/__setstate__) instead.
    def get_state(self):
        raise NotImplementedError(
            "ConditionalCovariance composes sub-models; use pickle, not get_state/set_state."
        )

    def set_state(self, state):
        raise NotImplementedError(
            "ConditionalCovariance composes sub-models; use pickle, not get_state/set_state."
        )

    def __getstate__(self) -> dict:
        return self.__dict__

    def __setstate__(self, data: dict) -> None:
        self.__dict__.update(data)

    def __repr__(self) -> str:
        vol = self.vol if not isinstance(self.vol, BaseOnlineCovariance) else repr(self.vol)
        return f"ConditionalCovariance(vol={vol}, corr={self.corr!r})"
