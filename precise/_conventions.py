"""Small shared conventions for the online covariance estimators.

Kept dependency-light: numpy only.
"""

from __future__ import annotations

import math
import numbers

import numpy as np

# An observation is a 1d vector; a batch is a 2d (n_samples, n_features) array.


def as_rows(X: list | np.ndarray) -> np.ndarray:
    """Coerce input to a 2d float array of rows.

    A 1d input is treated as a single observation (one row); a 2d input is a
    batch of observations, one per row. Mirrors the convention used by sklearn's
    ``partial_fit(X)`` while also supporting the one-observation streaming case.
    """
    arr = np.asarray(X, dtype=float)
    if arr.ndim == 1:
        return arr[np.newaxis, :]
    if arr.ndim == 2:
        return arr
    raise ValueError(f"Expected a 1d observation or 2d batch, got ndim={arr.ndim}.")


def check_rate(owner: str, name: str, value: object) -> None:
    """Raise ``ValueError`` unless ``value`` is a finite number in ``(0, 1]``.

    A decay rate is the weight of the newest observation, so the old estimate keeps ``1 - r``. Any
    rate outside ``(0, 1]`` makes one of those two weights negative (or, at zero, divides by it),
    and the recursion stops being a covariance: it can return an indefinite matrix that still
    looks finite and symmetric.
    """
    ok = isinstance(value, numbers.Real) and not isinstance(value, bool)
    if ok:
        v = float(value)  # type: ignore[arg-type]
        ok = math.isfinite(v) and 0.0 < v <= 1.0
    if not ok:
        raise ValueError(f"{owner}: {name} must be a finite number in (0, 1], got {value!r}.")
