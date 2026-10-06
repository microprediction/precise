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
import warnings

import numpy as np

from precise import _linalg
from precise._conventions import as_rows, check_rate


class NotFittedError(ValueError):
    """Raised when a fitted attribute is requested before any data has been seen."""


class BaseOnlineCovariance:
    """Base class for every online covariance estimator in precise.

    Not used directly: instantiate a subclass such as :class:`~precise.EwaCovariance`. A subclass
    implements ``_init_state(n_dim)``, returning the initial state as a plain dict of arrays and
    scalars, and ``_update_state(state, x)``, which folds in one observation ``x`` and returns the
    new state. It may override ``_state_to_cov`` to defer expensive work until ``covariance_`` is
    read. Everything else is inherited:

    * fitting: ``partial_fit(X)`` (one observation as a 1-D array, or a 2-D batch of rows) and
      ``fit(X)`` (reset, then fit a batch);
    * fitted attributes: ``covariance_``, ``correlation_``, ``precision_``, ``location_``,
      ``n_samples_``, ``n_features_in_``;
    * scoring: ``score(X)`` (mean Gaussian log-likelihood) and ``mahalanobis(X)``;
    * checkpointing: ``get_state()`` / ``set_state(state)``, with a JSON-friendly state;
    * sklearn-style ``get_params()`` / ``set_params(**params)``.

    Reading a fitted attribute before any data has been seen raises :class:`NotFittedError`.

    Example::

        >>> import numpy as np
        >>> from precise import EwaCovariance
        >>> est = EwaCovariance(r=0.05)
        >>> est.partial_fit(np.random.default_rng(0).standard_normal((100, 3)))
        EwaCovariance(...)
        >>> est.covariance_.shape
        (3, 3)
    """

    # Subclasses may set diff=True (in __init__) to estimate on first differences.

    def __init__(self) -> None:
        self._state: dict | None = None
        self.n_features_in_: int | None = None
        self._prev_x: np.ndarray | None = None  # for diff=True
        self._validate_params()

    def _validate_params(self) -> None:
        """Raise ``ValueError`` if a hyperparameter is outside its documented domain.

        Called on construction, by ``set_params``, and before every update, so a bad value fails
        at the source instead of surfacing later as an indefinite or silently different estimate.
        Subclasses with further constrained hyperparameters extend this and call ``super()``.
        """
        if "r" in self._param_names():
            check_rate(type(self).__name__, "r", getattr(self, "r", None))

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
        self._validate_params()
        rows = self._check_finite(self._check_n_features(as_rows(X)))
        use_diff = getattr(self, "diff", False)
        for x in rows:
            if use_diff:
                # Keep a copy: x may be a view of the caller's buffer, which they are free to reuse.
                if self._prev_x is None:
                    self._prev_x = x.copy()
                    continue
                x, self._prev_x = x - self._prev_x, x.copy()
            if self._state is None:
                self.n_features_in_ = len(x)
                self._state = self._init_state(len(x))
            self._state = self._update_state(self._state, x)
        return self

    def _check_n_features(self, rows: np.ndarray, expected: int | None = None) -> np.ndarray:
        """Return ``rows`` if their width matches the stream's fixed dimension, else raise.

        The positional estimators have a fixed dimension. Without this check numpy broadcasting
        quietly read a one-element row as the same value in every column, and a wider row expanded
        the estimate past ``n_features_in_``. Checked before any state is touched.
        """
        if expected is None:
            expected = self.n_features_in_
        if expected is None and self._prev_x is not None:  # diff=True, first level stored
            expected = len(self._prev_x)
        width = rows.shape[1]
        if len(rows) and width == 0:
            raise ValueError(f"{type(self).__name__}: an observation needs at least one feature.")
        if expected is not None and width != expected:
            raise ValueError(
                f"{type(self).__name__} has {expected} features but got rows with {width}. The "
                "positional estimators have a fixed dimension; use keyed(...) for a changing "
                "universe."
            )
        return rows

    def _check_finite(self, rows: np.ndarray) -> np.ndarray:
        """Return ``rows`` if every value is finite, else raise before any state is touched.

        One NaN or inf used to enter the running moments and stay there for good: the estimate
        stayed non-finite (or failed later inside a decomposition) however much clean data
        followed. Missing values need an explicit policy; the keyed adapters provide imputation.
        """
        bad = ~np.isfinite(rows)
        if bad.any():
            i, j = (int(v) for v in np.argwhere(bad)[0])
            raise ValueError(
                f"{type(self).__name__}: observations must be finite, got {rows[i, j]} in row {i}, "
                f"column {j}. Nothing was updated."
            )
        return rows

    def fit(self, X, y=None) -> BaseOnlineCovariance:
        """Reset and fit on a 2d batch ``X`` (sklearn drop-in)."""
        self._state = None
        self._prev_x = None
        arr = np.asarray(X, dtype=float)
        if arr.ndim != 2:
            raise ValueError("fit expects a 2d array of shape (n_samples, n_features).")
        return self.partial_fit(arr)

    def _fitted_state(self) -> dict:
        self._validate_params()  # a hyperparameter assigned after fitting is read here
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
    def _modeled_rows(self, X) -> np.ndarray:
        """Map rows in the input space of ``fit`` to the space the estimate describes.

        With ``diff=True`` the estimate is of first differences, so a batch of levels is
        differenced within itself: ``n`` rows give ``n - 1`` differences. Scoring raw levels
        against a difference model made the answer depend on arbitrary price origins.
        """
        rows = self._check_n_features(as_rows(X), expected=len(self.location_))
        if getattr(self, "diff", False):
            if len(rows) < 2:
                raise ValueError(
                    f"{type(self).__name__} was fitted with diff=True, so mahalanobis and score "
                    "take levels, as fit does, and difference them within the batch; pass at "
                    "least two consecutive rows."
                )
            rows = np.diff(rows, axis=0)
        return rows

    def _mahalanobis(self, rows: np.ndarray) -> np.ndarray:
        centered = rows - self.location_
        return np.einsum("ij,jk,ik->i", centered, self.precision_, centered)

    def mahalanobis(self, X) -> np.ndarray:
        """Squared Mahalanobis distance of each row of ``X`` from ``location_``.

        ``X`` is in the same space as for ``fit``. With ``diff=True`` that means levels, and the
        distances are those of the ``len(X) - 1`` first differences within ``X``.
        """
        return self._mahalanobis(self._modeled_rows(X))

    def score(self, X, y=None) -> float:
        """Mean Gaussian log-likelihood of the rows of ``X`` under the fitted estimate.

        ``X`` is in the same space as for ``fit``. With ``diff=True`` that means levels, and the
        score is the mean over the ``len(X) - 1`` first differences within ``X``.
        """
        rows = self._modeled_rows(X)
        _, logdet = np.linalg.slogdet(self.precision_)
        p = rows.shape[1]
        quad = self._mahalanobis(rows)
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
        old = {key: getattr(self, key) for key in params if hasattr(self, key)}
        for key, value in params.items():
            setattr(self, key, value)
        try:
            self._validate_params()
        except ValueError:
            for key in params:  # leave the estimator exactly as it was
                if key in old:
                    setattr(self, key, old[key])
                else:
                    delattr(self, key)
            raise
        return self

    # ------------------------------------------------------- serialization
    def get_state(self) -> dict | None:
        """Return the current state as a plain, JSON-friendly dict (or None if unfitted).

        With ``diff=True`` it also carries ``prev_x``, the last raw level, so that a stream resumed
        from the checkpoint forms the difference that crosses it.
        """
        state = None if self._state is None else self._export_state(self._state)
        if self._prev_x is not None:
            state = dict(state or {})
            state["prev_x"] = self._prev_x.tolist()
        return state

    def set_state(self, state: dict | None) -> BaseOnlineCovariance:
        """Restore state previously produced by :meth:`get_state`."""
        self._prev_x = None  # never carry a level over from whatever this object saw before
        if state is None:
            self._state = None
            self.n_features_in_ = None
            return self
        state = dict(state)
        prev = state.pop("prev_x", None)
        if prev is not None:
            self._prev_x = np.array(prev, dtype=float)
        elif getattr(self, "diff", False) and state:
            warnings.warn(
                f"{type(self).__name__}: this checkpoint has no prev_x (it predates diff=True "
                "checkpointing), so the difference across it cannot be formed and the next "
                "observation will only start a new one.",
                stacklevel=2,
            )
        self._state = self._import_state(state) if state else None
        n_dim = None if self._state is None else self._state.get("n_dim")
        self.n_features_in_ = None if n_dim is None else int(n_dim)
        return self

    def _export_state(self, state: dict) -> dict:
        return {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in state.items()}

    def _import_state(self, state: dict) -> dict:
        return {k: np.array(v, dtype=float) if isinstance(v, list) else v for k, v in state.items()}

    def __getstate__(self) -> dict:
        return {
            "params": self.get_params(),
            "state": self.get_state(),
            "n_features_in_": self.n_features_in_,
            "prev_x": None if self._prev_x is None else self._prev_x.tolist(),
        }

    def __setstate__(self, data: dict) -> None:
        self.__init__(**data["params"])  # type: ignore[misc]
        state, prev = data["state"], data.get("prev_x")
        if prev is not None:  # pickles made before get_state carried prev_x
            state = {**(state or {}), "prev_x": prev}
        self.set_state(state)
        self.n_features_in_ = data.get("n_features_in_")

    def __repr__(self) -> str:
        params = ", ".join(f"{k}={getattr(self, k)!r}" for k in self._param_names())
        return f"{type(self).__name__}({params})"
