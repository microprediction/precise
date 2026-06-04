"""Exponentially weighted partial-moment (semi-) covariance.

Decomposes each centered observation into the four sign quadrants and accumulates a
recency-weighted scatter for each, summing them into a covariance-like matrix. This
captures downside/upside co-movement structure that a plain covariance averages away.
The summed matrix is symmetrized and projected to the nearest positive-definite matrix.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import nearest_pos_def, to_symmetric
from precise._state import ewa_burn_n
from precise.base import BaseOnlineCovariance

# (sign for the first leg, sign for the second leg) of each quadrant's partial moment.
_QUADRANTS = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


class PartialMomentsCovariance(BaseOnlineCovariance):
    """Recency-weighted partial-moment (semi-)covariance.

    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, diff: bool = False):
        self.r = r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        # quadrants stacked as (4, n_dim, n_dim) so the state stays a plain (JSON-able) dict.
        return {
            "n_dim": n_dim,
            "n_samples": 0,
            "mean": np.zeros(n_dim),
            "quadrants": np.zeros((len(_QUADRANTS), n_dim, n_dim)),
            "r": self.r,
            "n_burn": ewa_burn_n(self.r),
        }

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        count = s["n_samples"] + 1
        # Centre on the running mean (empirical during burn-in, then exponential).
        if count <= s["n_burn"]:
            mean = s["mean"] + (x - s["mean"]) / count
        else:
            mean = (1 - s["r"]) * s["mean"] + s["r"] * x
        centered = x - s["mean"]

        prev = np.asarray(s["quadrants"], dtype=float)
        quadrants = np.empty_like(prev)
        for q, (sign1, sign2) in enumerate(_QUADRANTS):
            leg1 = np.clip(centered * sign1, 0, None) * sign1
            leg2 = np.clip(centered * sign2, 0, None) * sign2
            scatter = np.outer(leg1, leg2)
            if count <= s["n_burn"]:
                quadrants[q] = prev[q] + (scatter - prev[q]) / count
            else:
                quadrants[q] = (1 - s["r"]) * prev[q] + s["r"] * scatter

        return {
            "n_dim": s["n_dim"],
            "n_samples": count,
            "mean": mean,
            "quadrants": quadrants,
            "r": s["r"],
            "n_burn": s["n_burn"],
        }

    def _state_to_cov(self, state: dict) -> np.ndarray:
        total = np.asarray(state["quadrants"], dtype=float).sum(axis=0)
        return nearest_pos_def(to_symmetric(total))
