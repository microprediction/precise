"""The estimator contract: ``BaseOnlineCovariance``.

An sklearn-style online covariance estimator. Subclasses implement two hooks —
``_init_state(n_dim)`` and ``_update_state(state, x)`` — and inherit the full public
interface: ``partial_fit`` / ``fit`` and the fitted attributes ``covariance_``,
``correlation_``, ``precision_``, ``location_``, ``n_samples_``.

This mirrors the conventions of ``sklearn.covariance`` (whose estimators are batch-only
and lack ``partial_fit``) without importing or subclassing sklearn — numpy is the only
dependency. The functional update hooks keep the state a plain dict, so ``get_state`` /
``set_state`` give transparent mid-stream checkpointing.
"""

from __future__ import annotations

import inspect

import numpy as np

from precise import _linalg
from precise._conventions import as_rows


class NotFittedError(ValueError):
    """Raised when a fitted attribute is requested before any data has been seen."""


class BaseOnlineCovariance:
    # Subclasses may set diff=True (in __init__) to estimate on first differences.

    def __init__(self) -> None:
        self._state: dict | None = None
        self.n_features_in_: int | None = None
        self._prev_x: np.ndarray | None = None  # for diff=True

    # ------------------------------------------------------------------ hooks
    def _init_state(self, n_dim: int) -> dict:
        raise NotImplementedError

    def _update_state(self, state: dict, x: np.ndarray) -> dict:
        raise NotImplementedError

    def _state_to_cov(self, state: dict) -> np.ndarray:
        return state["cov"]

    def _state_to_mean(self, state: dict) -> np.ndarray:
        return state["mean"]

    # -------------------------------------------------------------- fitting
    def partial_fit(self, X, y=None) -> BaseOnlineCovariance:
        """Update the estimate with one observation (1d) or a batch of rows (2d)."""
        use_diff = getattr(self, "diff", False)
        for x in as_rows(X):
            if use_diff:
                if self._prev_x is None:
                    self._prev_x = x
                    continue
                x, self._prev_x = x - self._prev_x, x
            if self._state is None:
                self.n_features_in_ = len(x)
                self._state = self._init_state(len(x))
            self._state = self._update_state(self._state, x)
        return self

    def fit(self, X, y=None) -> BaseOnlineCovariance:
        """Reset and fit on a 2d batch ``X`` (sklearn drop-in)."""
        self._state = None
        self._prev_x = None
        arr = np.asarray(X, dtype=float)
        if arr.ndim != 2:
            raise ValueError("fit expects a 2d array of shape (n_samples, n_features).")
        return self.partial_fit(arr)

    def _fitted_state(self) -> dict:
        if self._state is None or self._state.get("n_samples", 0) < 1:
            raise NotFittedError(
                f"{type(self).__name__} has not seen any observations yet; "
                "call partial_fit or fit first."
            )
        return self._state

    # --------------------------------------------------- fitted attributes
    @property
    def n_samples_(self) -> int:
        return 0 if self._state is None else int(self._state["n_samples"])

    @property
    def location_(self) -> np.ndarray:
        return np.asarray(self._state_to_mean(self._fitted_state()), dtype=float)

    @property
    def covariance_(self) -> np.ndarray:
        cov = np.asarray(self._state_to_cov(self._fitted_state()), dtype=float)
        return _linalg.to_symmetric(cov)

    @property
    def correlation_(self) -> np.ndarray:
        return _linalg.cov_to_corrcoef(self.covariance_)

    @property
    def precision_(self) -> np.ndarray:
        return _linalg.try_invert(self.covariance_)

    def get_precision(self) -> np.ndarray:
        return self.precision_

    # ----------------------------------------------------------- scoring
    def mahalanobis(self, X) -> np.ndarray:
        """Squared Mahalanobis distance of each row of ``X`` from ``location_``."""
        rows = as_rows(X)
        prec = self.precision_
        centered = rows - self.location_
        return np.einsum("ij,jk,ik->i", centered, prec, centered)

    def score(self, X, y=None) -> float:
        """Mean Gaussian log-likelihood of the rows of ``X`` under the fitted estimate."""
        rows = as_rows(X)
        prec = self.precision_
        _, logdet = np.linalg.slogdet(prec)
        p = rows.shape[1]
        quad = self.mahalanobis(rows)
        ll = 0.5 * logdet - 0.5 * quad - 0.5 * p * np.log(2 * np.pi)
        return float(np.mean(ll))

    # ------------------------------------------------------------- params
    @classmethod
    def _param_names(cls) -> list:
        sig = inspect.signature(cls.__init__)
        return [p for p in sig.parameters if p != "self"]

    def get_params(self, deep: bool = True) -> dict:
        return {k: getattr(self, k) for k in self._param_names()}

    def set_params(self, **params) -> BaseOnlineCovariance:
        for key, value in params.items():
            setattr(self, key, value)
        return self

    # ------------------------------------------------------- serialization
    def get_state(self) -> dict | None:
        """Return the current state as a plain, JSON-friendly dict (or None if unfitted)."""
        if self._state is None:
            return None
        return {
            k: (v.tolist() if isinstance(v, np.ndarray) else v)
            for k, v in self._state.items()
        }

    def set_state(self, state: dict | None) -> BaseOnlineCovariance:
        """Restore state previously produced by :meth:`get_state`."""
        if state is None:
            self._state = None
            self.n_features_in_ = None
            return self
        restored = {}
        for k, v in state.items():
            restored[k] = np.array(v, dtype=float) if isinstance(v, list) else v
        self._state = restored
        n_dim = restored.get("n_dim")
        self.n_features_in_ = None if n_dim is None else int(n_dim)
        return self

    def __getstate__(self) -> dict:
        return {
            "params": self.get_params(),
            "state": self.get_state(),
            "n_features_in_": self.n_features_in_,
            "prev_x": None if self._prev_x is None else self._prev_x.tolist(),
        }

    def __setstate__(self, data: dict) -> None:
        self.__init__(**data["params"])  # type: ignore[misc]
        self.set_state(data["state"])
        self.n_features_in_ = data.get("n_features_in_")
        prev = data.get("prev_x")
        self._prev_x = None if prev is None else np.array(prev, dtype=float)

    def __repr__(self) -> str:
        params = ", ".join(f"{k}={getattr(self, k)!r}" for k in self._param_names())
        return f"{type(self).__name__}({params})"
