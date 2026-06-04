"""Diagonal online covariance — per-variable variances only, zero off-diagonal.

Assumes the variables are uncorrelated: it tracks only the marginal (recency-weighted) variances,
so the update is O(d) per step. Useful as a cheap baseline and bake-off contestant — and a sensible
fallback when there are too few observations to estimate correlations reliably.
"""

from __future__ import annotations

import numpy as np

from precise._state import ewa_burn_n
from precise.base import BaseOnlineCovariance


class DiagonalCovariance(BaseOnlineCovariance):
    """Online diagonal covariance (independent variables).

    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, diff: bool = False):
        self.r = r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return {
            "n_dim": n_dim,
            "n_samples": 0,
            "mean": np.zeros(n_dim),
            "var": np.zeros(n_dim),
            "r": float(self.r),
            "n_burn": ewa_burn_n(self.r),
        }

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        n = s["n_samples"] + 1
        dev = x - s["mean"]
        sq = dev * dev
        if n <= s["n_burn"]:
            mean = s["mean"] + dev / n
            var = s["var"] + (sq - s["var"]) / n
        else:
            mean = (1 - s["r"]) * s["mean"] + s["r"] * x
            var = (1 - s["r"]) * s["var"] + s["r"] * sq
        return {
            "n_dim": s["n_dim"],
            "n_samples": n,
            "mean": mean,
            "var": var,
            "r": s["r"],
            "n_burn": s["n_burn"],
        }

    def _state_to_cov(self, state: dict) -> np.ndarray:
        return np.diag(np.asarray(state["var"], dtype=float))

    def _state_to_mean(self, state: dict) -> np.ndarray:
        return np.asarray(state["mean"], dtype=float)
