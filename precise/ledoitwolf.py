"""Online Ledoit-Wolf shrinkage covariance.

A truly online estimator (O(d^2) per step, no stored window): it maintains an
exponentially weighted sample covariance and tracks the Ledoit & Wolf (2004) shrinkage
quantities incrementally, shrinking towards a scaled identity. The shrinkage intensity is
recomputed on demand from the running statistics. numpy only — no scikit-learn dependency.
"""

from __future__ import annotations

import numpy as np

from precise._state import emp_update, ewa_init
from precise.base import BaseOnlineCovariance


class LedoitWolfCovariance(BaseOnlineCovariance):
    """Online Ledoit-Wolf shrinkage covariance.

    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, diff: bool = False):
        self.r = r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        s = ewa_init(n_dim, self.r)
        s["pi_bar"] = 0.0  # running mean dispersion of the per-sample scatter about cov
        return s

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        if s["n_samples"] < s["n_burn"]:
            out = emp_update(s, x)
            out["r"], out["n_burn"], out["pi_bar"] = s["r"], s["n_burn"], s["pi_bar"]
            return out
        r = s["r"]
        p = s["n_dim"]
        delta = x - s["mean"]
        scatter = np.outer(delta, delta)
        q = np.sum((scatter - s["cov"]) ** 2) / p  # squared dispersion of this scatter
        return {
            "n_dim": p,
            "n_samples": s["n_samples"] + 1,
            "mean": (1 - r) * s["mean"] + r * x,
            "cov": (1 - r) * s["cov"] + r * scatter,
            "r": r,
            "n_burn": s["n_burn"],
            "pi_bar": (1 - r) * s["pi_bar"] + r * q,
        }

    def _state_to_cov(self, state: dict) -> np.ndarray:
        S = np.asarray(state["cov"], dtype=float)
        p = state["n_dim"]
        mu = np.trace(S) / p
        d2 = np.sum((S - mu * np.eye(p)) ** 2) / p
        if d2 <= 0 or state.get("pi_bar", 0.0) <= 0:
            return S
        # Effective sample size of the EWA is ~ 1/r, so b^2 ~ pi_bar * r.
        b2 = min(state["pi_bar"] * state["r"], d2)
        intensity = float(np.clip(b2 / d2, 0.0, 1.0))
        return (1 - intensity) * S + intensity * mu * np.eye(p)
