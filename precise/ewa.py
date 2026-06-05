"""Exponentially weighted online covariance (RiskMetrics-style).

A recency-weighted estimate that decays past observations at rate ``r`` per step, after
a short empirical burn-in so the estimate does not start degenerate.
"""

from __future__ import annotations

import numpy as np

from precise._state import ewa_init, ewa_update
from precise.base import BaseOnlineCovariance


class EwaCovariance(BaseOnlineCovariance):
    """Exponentially weighted moving-average covariance.

    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
                  Smaller ``r`` = longer memory.
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, diff: bool = False):
        self.r = r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return ewa_init(n_dim, self.r)

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        return ewa_update(s, x)
