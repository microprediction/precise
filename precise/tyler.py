"""Recursive Tyler M-estimator — robust shape / correlation.

Tyler's M-estimator is the "most robust" estimator of scatter for elliptically-distributed data:
it is distribution-free over the elliptical family (it depends only on the *directions* of the
centered observations, not their magnitudes), so heavy tails and gross outliers barely move it. This
is the recursive/online form. Because Tyler's estimator determines scatter only up to scale, the
reported ``covariance_`` is normalized to unit diagonal — i.e. it is a **robust correlation**. For a
calibrated covariance, compose it with a volatility model via
:class:`~precise.conditional.ConditionalCovariance` (``corr=TylerCovariance()``).
"""

from __future__ import annotations

import numpy as np

from precise._linalg import cov_to_corrcoef, try_invert
from precise._state import ewa_burn_n
from precise.base import BaseOnlineCovariance


class TylerCovariance(BaseOnlineCovariance):
    """Online (recursive) Tyler M-estimator of shape; ``covariance_`` is a robust correlation.

    :param r:     Decay rate, in (0, 1].
    :param diff:  If ``True``, estimate on first differences of the stream.
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
            "C": np.eye(n_dim),  # shape matrix, normalized to trace == n_dim
            "r": float(self.r),
            "n_burn": ewa_burn_n(self.r),
        }

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        p = s["n_dim"]
        n = s["n_samples"] + 1
        if n <= s["n_burn"]:
            lr = 1.0 / n
            mean = s["mean"] + (x - s["mean"]) / n
        else:
            lr = s["r"]
            mean = (1 - s["r"]) * s["mean"] + s["r"] * x
        dev = x - s["mean"]
        C = np.asarray(s["C"], dtype=float)
        q = max(float(dev @ try_invert(C) @ dev), 1e-12)  # Mahalanobis under the current shape
        C = (1 - lr) * C + lr * p * np.outer(dev, dev) / q  # direction-only contribution
        C = p * C / np.trace(C)  # fix the scale: trace == p
        return {
            "n_dim": p, "n_samples": n, "mean": mean, "C": C, "r": s["r"], "n_burn": s["n_burn"],
        }

    def _state_to_cov(self, state: dict) -> np.ndarray:
        return cov_to_corrcoef(np.asarray(state["C"], dtype=float))

    def _state_to_mean(self, state: dict) -> np.ndarray:
        return np.asarray(state["mean"], dtype=float)
