"""Small shared conventions for the online covariance estimators.

Kept dependency-light: numpy only.
"""

from __future__ import annotations

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
