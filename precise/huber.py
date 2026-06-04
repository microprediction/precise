"""Robust online covariance using a Huber location estimate.

A rolling-window estimator that resists outliers by computing covariance entries as a
robust (Huber M-estimator) location of the per-observation scatter products, rather than a
plain average. The result is projected to the nearest positive-definite matrix. Numpy only.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import huber_location, nearest_pos_def, to_symmetric
from precise.base import BaseOnlineCovariance


class HuberCovariance(BaseOnlineCovariance):
    """Robust online covariance over a rolling window.

    :param window:  Number of most-recent observations to estimate from.
    :param c:       Huber tuning constant (in robust standard deviations); smaller is more robust.
    :param diff:    If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, window: int = 100, c: float = 1.345, diff: bool = False):
        self.window = window
        self.c = c
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return {
            "n_dim": n_dim,
            "n_samples": 0,
            "mean": np.zeros(n_dim),
            "cov": np.eye(n_dim),
            "buffer": [],
        }

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        n_dim = s["n_dim"]
        buffer = list(s["buffer"])
        buffer.append(np.asarray(x, dtype=float).tolist())
        if len(buffer) > self.window:
            buffer = buffer[-self.window :]
        rows = np.array(buffer, dtype=float)

        if len(buffer) <= 2:
            mean = rows.mean(axis=0)
            cov = np.eye(n_dim)
        else:
            mean = huber_location(rows, c=self.c)
            centered = rows - mean
            # Robust location of the flattened scatter products x_k x_k^T.
            scatter = (centered[:, :, None] * centered[:, None, :]).reshape(
                len(buffer), n_dim * n_dim
            )
            cov = nearest_pos_def(to_symmetric(huber_location(scatter, c=self.c).reshape(n_dim, n_dim)))

        return {
            "n_dim": n_dim,
            "n_samples": s["n_samples"] + 1,
            "mean": mean,
            "cov": cov,
            "buffer": buffer,
        }
