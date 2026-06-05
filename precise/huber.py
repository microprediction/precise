"""Robust online covariance via an exponentially weighted Huber M-estimator.

A truly online estimator (O(d^3) per step for the Mahalanobis weight, no stored window):
each new observation is downweighted by its Mahalanobis distance under the current estimate
before being folded into a recency-weighted mean and covariance, so isolated outliers cannot
dominate. numpy only.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import try_invert
from precise._state import emp_update, ewa_init
from precise.base import BaseOnlineCovariance


class HuberCovariance(BaseOnlineCovariance):
    """Online robust covariance with Huber downweighting of outliers.

    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
    :param c:     Mahalanobis cutoff (in standard deviations); observations beyond it are
                  downweighted. Smaller ``c`` is more robust.
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, c: float = 2.5, diff: bool = False):
        self.r = r
        self.c = c
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return ewa_init(n_dim, self.r)

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        if s["n_samples"] < s["n_burn"]:
            out = emp_update(s, x)
            out["r"], out["n_burn"] = s["r"], s["n_burn"]
            return out
        r = s["r"]
        p = s["n_dim"]
        delta = x - s["mean"]
        # Multivariate Huber weight from the Mahalanobis distance under the current estimate.
        maha2 = float(delta @ try_invert(s["cov"]) @ delta)
        threshold = (self.c**2) * p
        w = 1.0 if maha2 <= threshold else np.sqrt(threshold / maha2)
        weighted = w * delta
        return {
            "n_dim": p,
            "n_samples": s["n_samples"] + 1,
            "mean": s["mean"] + r * weighted,
            "cov": (1 - r) * s["cov"] + r * np.outer(weighted, weighted),
            "r": r,
            "n_burn": s["n_burn"],
        }
