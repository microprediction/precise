"""Adapters that turn a positional covariance estimator into a river-compatible dict estimator.

The estimators in this package are *positional*: ``partial_fit`` takes a fixed-length vector
whose slots have fixed meaning. In streaming/finance settings observations instead arrive as
**dicts keyed by name**, and the set of names may change over time. This module provides a small
collection of adapters that decorate any positional :class:`~precise.base.BaseOnlineCovariance`
(passed as a configured instance, cloned per use via ``get_params``) to consume keyed dicts and
emit keyed output — a river-style ``learn_one(x)`` / ``.covariance`` surface.

Two adapters, by how they treat the universe of names:

* :class:`FixedUniverse` — a **fixed** named universe: one wrapped estimator; occasional missing
  keys are imputed. Unbiased when all keys are present; cannot add genuinely new names.
* :class:`DynamicUniverse` — a **changing** universe: names enter and leave freely, handled with
  a multi-universe strategy (one wrapped estimator per key-set), assembling a matrix per query.

Both add no covariance math of their own — they delegate entirely to the wrapped estimator.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import cov_to_corrcoef, nearest_pos_def, to_symmetric
from precise.base import BaseOnlineCovariance
from precise.ewa import EwaCovariance


def _clone(estimator: BaseOnlineCovariance) -> BaseOnlineCovariance:
    """A fresh, unfitted copy of a configured estimator (same params, no state)."""
    return type(estimator)(**estimator.get_params())


def _factory(estimator, kwargs):
    """Build a zero-arg factory from either a configured instance or a class + kwargs."""
    if isinstance(estimator, type):
        return lambda: estimator(**kwargs)
    if kwargs:
        raise ValueError("Pass estimator keyword arguments only with a class, not an instance.")
    return lambda: _clone(estimator)


class _KeyedAdapter:
    """Shared river-compatible surface for the keyed adapters.

    Subclasses implement :meth:`update` and :meth:`cov_array` (returning ``(matrix, keys)``).
    """

    # --- streaming (river verbs) ---
    def update(self, x: dict):  # pragma: no cover - implemented by subclasses
        raise NotImplementedError

    def learn_one(self, x: dict):
        return self.update(x)

    def learn_many(self, X):
        for x in X:
            self.update(x)
        return self

    # --- assembly (implemented by subclasses) ---
    def cov_array(self, keys=None):  # pragma: no cover - implemented by subclasses
        raise NotImplementedError

    def get_cov(self, keys=None) -> np.ndarray:
        return self.cov_array(keys)[0]

    def get_corr(self, keys=None) -> np.ndarray:
        cov, _ = self.cov_array(keys)
        corr = cov_to_corrcoef(cov)
        np.fill_diagonal(corr, 1.0)
        return corr

    @staticmethod
    def _as_dict_of_dicts(matrix, keys) -> dict[str, dict[str, float]]:
        return {
            ki: {kj: float(matrix[i, j]) for j, kj in enumerate(keys)}
            for i, ki in enumerate(keys)
        }

    # --- fitted attributes (keyed output) ---
    @property
    def covariance_(self) -> dict[str, dict[str, float]]:
        cov, keys = self.cov_array()
        return self._as_dict_of_dicts(cov, keys)

    @property
    def correlation_(self) -> dict[str, dict[str, float]]:
        cov, keys = self.cov_array()
        corr = cov_to_corrcoef(cov)
        np.fill_diagonal(corr, 1.0)
        return self._as_dict_of_dicts(corr, keys)

    # river-style alias
    @property
    def covariance(self) -> dict[str, dict[str, float]]:
        return self.covariance_

    def to_frame(self, keys=None):
        """Covariance as a pandas ``DataFrame`` (requires the ``[pandas]`` extra)."""
        try:
            import pandas as pd
        except ImportError as exc:  # pragma: no cover - only without pandas
            raise ImportError(
                "to_frame requires pandas. Install with: pip install precise[pandas]"
            ) from exc
        cov, keys = self.cov_array(keys)
        return pd.DataFrame(cov, index=keys, columns=keys)


class FixedUniverse(_KeyedAdapter):
    """Decorate a positional estimator for a **fixed** named universe (river-style dict API).

    The universe is the key-set of the first observation (or ``keys`` if given). Observations
    missing some of those keys are imputed; genuinely new keys are ignored. For a universe whose
    membership actually changes, use :class:`DynamicUniverse` instead.

    :param estimator:  A configured positional estimator instance to wrap (default
                       ``EwaCovariance()``), or an estimator class (with ``**estimator_kwargs``).
    :param keys:       The fixed universe of names. If ``None``, taken from the first observation.
    :param impute:     How to fill a missing key: ``"ffill"`` (last seen value, default),
                       ``"mean"`` (current running mean), or ``"zero"``.
    """

    def __init__(self, estimator=None, *, keys=None, impute: str = "ffill", **estimator_kwargs):
        if estimator is None:
            estimator = EwaCovariance()
        self._make = _factory(estimator, estimator_kwargs)
        self.keys: list[str] | None = list(keys) if keys is not None else None
        self.impute = impute
        self._est: BaseOnlineCovariance | None = None
        self._last: np.ndarray | None = None

    def update(self, x: dict) -> FixedUniverse:
        if self.keys is None:
            self.keys = list(x.keys())
        if self._est is None:
            self._est = self._make()
            self._last = np.zeros(len(self.keys))
        assert self._last is not None  # set above on first update
        y = np.empty(len(self.keys))
        for i, k in enumerate(self.keys):
            if k in x:
                y[i] = x[k]
                self._last[i] = x[k]
            elif self.impute == "ffill":
                y[i] = self._last[i]
            elif self.impute == "mean":
                y[i] = self._est.location_[i] if self._est.n_samples_ > 0 else self._last[i]
            else:  # "zero"
                y[i] = 0.0
        self._est.partial_fit(y)
        return self

    def cov_array(self, keys=None):
        if self._est is None or self.keys is None:
            raise ValueError("No observation has been seen yet.")
        cov = self._est.covariance_
        if keys is None or list(keys) == self.keys:
            return cov, list(self.keys)
        idx = [self.keys.index(k) for k in keys]
        return cov[np.ix_(idx, idx)], list(keys)

    def __repr__(self) -> str:
        return f"FixedUniverse(keys={self.keys}, impute={self.impute!r})"


class _Universe:
    """A fixed set of keys with a wrapped online positional estimator. No buffer."""

    def __init__(self, keys, factory):
        self.keys: list[str] = list(keys)
        self.keys_set = set(self.keys)
        self.staleness = 0
        self.longevity = 0
        self._est: BaseOnlineCovariance = factory()

    def update(self, x: dict) -> None:
        y = np.array([x[k] for k in self.keys], dtype=float)
        self._est.partial_fit(y)
        self.staleness = 0
        self.longevity += 1

    @property
    def running_cov(self) -> np.ndarray | None:
        return self._est.covariance_ if self._est.n_samples_ > 0 else None


class DynamicUniverse(_KeyedAdapter):
    """Decorate a positional estimator for a **changing** named universe (river-style dict API).

    Names may enter and leave freely. Internally a universe (a wrapped estimator over a fixed
    column ordering) is kept per distinct key-set; a universe is updated whenever the observation
    contains all of its keys, otherwise it accrues staleness and is eventually evicted. A matrix is
    assembled per query by reading each pair from the longest-lived, least-stale universe that
    contains both, filling never-co-observed pairs with the grand off-diagonal mean and projecting
    to the nearest positive-definite matrix. Everything is online — no replay buffers.

    :param estimator:      A configured positional estimator instance to wrap (default
                           ``EwaCovariance()``), or an estimator class (with kwargs).
    :param max_universes:  Maximum number of universes to maintain concurrently.
    :param max_staleness:  Drop a universe after this many updates without usable data.
    """

    def __init__(
        self,
        estimator=None,
        *,
        max_universes: int = 10,
        max_staleness: int = 50,
        **estimator_kwargs,
    ):
        if estimator is None:
            estimator = EwaCovariance()
        self._make = _factory(estimator, estimator_kwargs)
        self.max_universes = max_universes
        self.max_staleness = max_staleness
        self.states: dict[int, _Universe] = {}
        self.x: dict | None = None
        self._counter = 0

    def _add_universe(self, universe: _Universe) -> None:
        self.states[self._counter] = universe
        self._counter += 1

    def update(self, x: dict) -> DynamicUniverse:
        self.x = dict(x)
        x_keys = set(x.keys())

        for universe in self.states.values():
            if universe.keys_set.issubset(x_keys):
                universe.update(x)
            else:
                universe.staleness += 1

        for ndx in [n for n, u in self.states.items() if u.staleness > self.max_staleness]:
            del self.states[ndx]

        if x_keys not in [u.keys_set for u in self.states.values()]:
            fresh = _Universe(keys=x.keys(), factory=self._make)
            fresh.update(x)
            self._add_universe(fresh)
            if len(self.states) > self.max_universes:
                victim = sorted(
                    self.states.items(), key=lambda kv: (-kv[1].staleness, kv[1].longevity)
                )[0][0]
                del self.states[victim]
        return self

    def _resolve_keys(self, keys) -> list[str]:
        if keys is not None:
            return list(keys)
        if self.x is None:
            raise ValueError("No keys supplied and no observation has been seen yet.")
        return list(self.x.keys())

    def cov_array(self, keys=None):
        keys = self._resolve_keys(keys)
        n = len(keys)
        idx = {k: i for i, k in enumerate(keys)}
        M = np.full((n, n), np.nan)
        for i, ki in enumerate(keys):
            for kj in keys[i:]:
                candidates = [
                    u
                    for u in self.states.values()
                    if {ki, kj}.issubset(u.keys_set) and u.running_cov is not None
                ]
                if candidates:
                    u = max(candidates, key=lambda u: (u.longevity, -u.staleness))
                    cov = u.running_cov
                    assert cov is not None  # guaranteed by the candidate filter
                    a, b = u.keys.index(ki), u.keys.index(kj)
                    M[idx[ki], idx[kj]] = M[idx[kj], idx[ki]] = cov[a, b]
        off_diag = M[~np.eye(n, dtype=bool)]
        fill = np.nanmean(off_diag) if np.any(~np.isnan(off_diag)) else 0.0
        if np.isnan(fill):
            fill = 0.0
        M = np.where(np.isnan(M), fill, M)
        return nearest_pos_def(to_symmetric(M)), keys

    def __repr__(self) -> str:
        return f"DynamicUniverse(universes={len(self.states)})"


def keyed(estimator=None, *, dynamic: bool = False, **kwargs) -> _KeyedAdapter:
    """Turn a positional covariance estimator into a river-compatible keyed (dict) estimator.

    The front door to the keyed adapters::

        from precise import keyed, EwaCovariance
        k = keyed(EwaCovariance(r=0.05))                 # FixedUniverse (imputes missing keys)
        d = keyed(EwaCovariance(r=0.05), dynamic=True)   # DynamicUniverse (names enter/leave)

        for x in stream:        # x = {"AAPL": 0.01, "MSFT": -0.02}
            d.learn_one(x)
        d.covariance_           # dict-of-dicts;  d.to_frame() for a pandas DataFrame

    :param estimator:  A configured positional estimator instance (default ``EwaCovariance()``),
                       or an estimator class (with ``**kwargs`` forwarded to it).
    :param dynamic:    ``False`` (default) → :class:`FixedUniverse`; ``True`` → a changing universe
                       (:class:`DynamicUniverse`).
    :param kwargs:     Adapter options — ``keys`` / ``impute`` for the fixed case,
                       ``max_universes`` / ``max_staleness`` for the dynamic case (or estimator
                       kwargs if a class was passed).
    """
    if dynamic:
        return DynamicUniverse(estimator, **kwargs)
    return FixedUniverse(estimator, **kwargs)
