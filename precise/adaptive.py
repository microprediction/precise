"""Adaptive-forgetting exponentially weighted covariance.

A plain EWMA must commit to one decay rate ``r`` — fast (noisy, but reacts to regime change) or
slow (smooth, but laggy). ``AdaptiveEwaCovariance`` adapts ``r`` per step: when an observation is
"surprising" (large Mahalanobis distance under the current estimate, the hallmark of a regime
change) it forgets faster; in calm periods it relaxes back to the baseline. Fully online.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import try_invert
from precise._state import emp_update, ewa_init
from precise.base import BaseOnlineCovariance


class AdaptiveEwaCovariance(BaseOnlineCovariance):
    """EWMA covariance with a forgetting rate that adapts to regime change.

    :param r:      Baseline decay rate (used in calm periods), in (0, 1].
    :param max_r:  Maximum decay rate when an observation is highly surprising.
    :param diff:   If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, max_r: float = 0.5, diff: bool = False):
        self.r = r
        self.max_r = max_r
        self.diff = diff
        super().__init__()

    # Rate at which the surprise signal is smoothed: a regime change is *sustained* surprise,
    # so we drive the forgetting rate off a smoothed ratio rather than a single (possibly outlier)
    # observation — otherwise one spike would overshoot.
    _DETECT = 0.1

    def _init_state(self, n_dim: int) -> dict:
        s = ewa_init(n_dim, self.r)
        s["max_r"] = float(self.max_r)
        s["sbar"] = 1.0  # smoothed surprise (1.0 == "as expected")
        return s

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        if s["n_samples"] < s["n_burn"]:
            out = emp_update(s, x)
            out["r"], out["n_burn"], out["max_r"], out["sbar"] = (
                s["r"], s["n_burn"], s["max_r"], s["sbar"],
            )
            return out
        p = s["n_dim"]
        base = s["r"]
        dev = x - s["mean"]
        # Surprise = Mahalanobis distance under the current estimate; ~p when "as expected".
        maha2 = float(dev @ try_invert(s["cov"]) @ dev)
        ratio = maha2 / p if p > 0 else 1.0
        sbar = (1 - self._DETECT) * s["sbar"] + self._DETECT * ratio
        r_eff = min(max(base * sbar, base), s["max_r"])
        return {
            "n_dim": p,
            "n_samples": s["n_samples"] + 1,
            "mean": (1 - r_eff) * s["mean"] + r_eff * x,
            "cov": (1 - r_eff) * s["cov"] + r_eff * np.outer(dev, dev),
            "r": base,
            "n_burn": s["n_burn"],
            "max_r": s["max_r"],
            "sbar": sbar,
        }
