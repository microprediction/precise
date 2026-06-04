"""Online Ledoit-Wolf shrinkage covariance.

A rolling-window estimator that applies Ledoit & Wolf (2004) linear shrinkage towards a
scaled identity on the most recent ``window`` observations. Pulls the shrinkage intensity
out of the data automatically; numpy only (no scikit-learn dependency).
"""

from __future__ import annotations

import numpy as np

from precise._linalg import ledoit_wolf
from precise.base import BaseOnlineCovariance


class LedoitWolfCovariance(BaseOnlineCovariance):
    """Online Ledoit-Wolf shrinkage covariance over a rolling window.

    :param window:  Number of most-recent observations to estimate from.
    :param diff:    If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, window: int = 100, diff: bool = False):
        self.window = window
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return {
            "n_dim": n_dim,
            "n_samples": 0,
            "mean": np.zeros(n_dim),
            "cov": np.eye(n_dim),
            "buffer": [],
            "shrinkage": 0.0,
        }

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        buffer = list(s["buffer"])
        buffer.append(np.asarray(x, dtype=float).tolist())
        if len(buffer) > self.window:
            buffer = buffer[-self.window :]
        rows = np.array(buffer, dtype=float)
        mean = rows.mean(axis=0)
        if len(buffer) >= 2:
            cov, intensity = ledoit_wolf(rows)
        else:
            cov, intensity = np.eye(s["n_dim"]), 0.0
        return {
            "n_dim": s["n_dim"],
            "n_samples": s["n_samples"] + 1,
            "mean": mean,
            "cov": np.atleast_2d(cov),
            "buffer": buffer,
            "shrinkage": float(intensity),
        }
