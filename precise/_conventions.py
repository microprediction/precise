"""Small shared conventions for the online covariance estimators.

Kept dependency-light: numpy only.
"""

from __future__ import annotations

import numpy as np

# An observation is a 1d vector; a batch is a 2d (n_samples, n_features) array.


def infer_dimension(n_dim: int | None = None, x: list | np.ndarray | None = None) -> int:
    """Infer the number of variables from either an explicit dimension or a sample.

    :param n_dim:  Explicit number of variables, if known.
    :param x:      A single observation (used only for its length) or an int dimension.
    :return:       The number of variables.
    """
    if n_dim is not None:
        return int(n_dim)
    if isinstance(x, int):
        return x
    if x is not None and len(x) >= 1:
        return len(x)
    raise ValueError("Ambiguous dimension. Supply an observation y or n_dim.")


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
