"""Dynamic Conditional Correlation (DCC) online covariance.

Engle's (2002) DCC decouples *volatility* from *correlation*: each series gets its own
exponentially weighted variance, and the correlation is an exponentially weighted average of the
*standardized* residuals, recombined as ``H = D R D`` with ``D = diag(sqrt(variances))``. This lets
volatility and correlation evolve on (optionally) different timescales — structure a single EWMA
covariance cannot capture. Fully online (O(d^2) per step, no stored window).
"""

from __future__ import annotations

import numpy as np

from precise._state import emp_init, ewa_burn_n
from precise.base import BaseOnlineCovariance


class DCCCovariance(BaseOnlineCovariance):
    """Online DCC covariance.

    :param r:      Decay rate for the correlation (quasi-correlation EWMA), in (0, 1].
    :param vol_r:  Decay rate for the per-series volatilities. Defaults to ``r``.
    :param diff:   If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, vol_r: float | None = None, diff: bool = False):
        self.r = r
        self.vol_r = vol_r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        s = emp_init(n_dim)
        s["h"] = np.ones(n_dim)  # per-series variances
        s["Q"] = np.eye(n_dim)  # quasi-correlation
        s["r"] = float(self.r)
        s["vol_r"] = float(self.vol_r if self.vol_r is not None else self.r)
        s["n_burn"] = ewa_burn_n(min(s["r"], s["vol_r"]))
        return s

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        p = s["n_dim"]
        n = s["n_samples"] + 1
        r, rv, n_burn = s["r"], s["vol_r"], s["n_burn"]
        dev = x - s["mean"]  # innovation about the prior mean

        if n <= n_burn:
            mean = s["mean"] + dev / n
            h = s["h"] + (dev * dev - s["h"]) / n
        else:
            mean = (1 - rv) * s["mean"] + rv * x
            h = (1 - rv) * s["h"] + rv * (dev * dev)

        eps = dev / np.sqrt(np.maximum(h, 1e-12))  # standardized residual
        outer = np.outer(eps, eps)
        if n <= n_burn:
            Q = s["Q"] + (outer - s["Q"]) / n
        else:
            Q = (1 - r) * s["Q"] + r * outer

        return {
            "n_dim": p,
            "n_samples": n,
            "mean": mean,
            "h": h,
            "Q": Q,
            "r": r,
            "vol_r": rv,
            "n_burn": n_burn,
        }

    def _state_to_cov(self, state: dict) -> np.ndarray:
        Q = np.asarray(state["Q"], dtype=float)
        h = np.asarray(state["h"], dtype=float)
        q_inv = 1.0 / np.sqrt(np.maximum(np.diag(Q), 1e-12))
        R = Q * np.outer(q_inv, q_inv)  # correlation from the quasi-correlation
        d = np.sqrt(np.maximum(h, 1e-12))
        return R * np.outer(d, d)  # H = D R D
