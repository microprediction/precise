"""Online Schur--Ledoit-Wolf covariance: analytic, data-estimated cross-block damping.

Like :class:`SchurCovariance`, but the cross-block coupling damping ``gamma`` is not a
hyperparameter -- it is *estimated* as the Ledoit & Wolf (2004) reliability of the
cross-block coupling. Shrinking the cross-block entries toward zero, the Frobenius-optimal
keep fraction is

    gamma* = sum_cross sigma_ij^2 / sum_cross ( sigma_ij^2 + Var(s_ij) )
           = 1 - (Ledoit-Wolf shrinkage intensity restricted to the cross-block block),

which is exactly the *coupling reliability*: it is small when the cross-block coupling is
dominated by sampling noise and tends to 1 as it becomes well estimated, so the damping
adapts to the effective sample size with no tuning. The required dispersion statistic is
tracked incrementally (O(d^2) per step), in the manner of :class:`LedoitWolfCovariance`.
At ``gamma_ -> 0`` the estimate is block-diagonal (HRP-like); at ``gamma_ -> 1`` it is the
full EWA covariance. numpy only.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import make_pos_def, to_symmetric
from precise._state import emp_update, ewa_init
from precise.base import BaseOnlineCovariance


class SchurLedoitWolfCovariance(BaseOnlineCovariance):
    """Online Schur covariance with a Ledoit-Wolf-estimated cross-block damping.

    :param r:         Decay rate of the underlying EWA covariance, in (0, 1].
    :param n_blocks:  Number of contiguous blocks to partition the variables into.
    :param diff:      If ``True``, estimate the covariance of first differences of the stream.

    After fitting, the data-estimated damping is available as ``self.gamma_``.
    """

    def __init__(self, r: float = 0.05, n_blocks: int = 4, diff: bool = False):
        self.r = r
        self.n_blocks = n_blocks
        self.diff = diff
        self.gamma_: float | None = None
        super().__init__()

    def _cross_mask(self, p: int) -> np.ndarray:
        nb = min(self.n_blocks, p)
        block_id = np.empty(p, dtype=int)
        for bi, idx in enumerate(np.array_split(np.arange(p), nb)):
            block_id[idx] = bi
        return block_id[:, None] != block_id[None, :]

    def _init_state(self, n_dim: int) -> dict:
        # State holds only plain accumulators (roundtrip-safe); the block mask is derived
        # from n_dim and n_blocks on demand, exactly as SchurCovariance does.
        s = ewa_init(n_dim, self.r)
        s["pi_cross"] = 0.0                       # EWA mean cross-block scatter dispersion
        return s

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        if s["n_samples"] < s["n_burn"]:
            out = emp_update(s, x)
            out["r"], out["n_burn"], out["pi_cross"] = s["r"], s["n_burn"], s["pi_cross"]
            return out
        r = s["r"]
        cross = self._cross_mask(s["n_dim"])
        delta = x - s["mean"]
        scatter = np.outer(delta, delta)
        q = float(np.sum(((scatter - s["cov"]) ** 2)[cross]))   # cross-block dispersion, this step
        return {
            "n_dim": s["n_dim"],
            "n_samples": s["n_samples"] + 1,
            "mean": (1 - r) * s["mean"] + r * x,
            "cov": (1 - r) * s["cov"] + r * scatter,
            "r": r,
            "n_burn": s["n_burn"],
            "pi_cross": (1 - r) * s["pi_cross"] + r * q,
        }

    def _state_to_cov(self, state: dict) -> np.ndarray:
        cov = np.asarray(state["cov"], dtype=float)
        cross = self._cross_mask(state["n_dim"])
        m2 = float(np.sum((cov ** 2)[cross]))               # ~ sum (sigma^2 + Var) over cross
        b2 = float(state.get("pi_cross", 0.0)) * state["r"]  # ~ sum Var(s) over cross (eff n ~ 1/r)
        gamma = float(np.clip(1.0 - b2 / m2, 0.0, 1.0)) if m2 > 0 else 1.0
        self.gamma_ = gamma
        out = cov.copy()
        out[cross] *= gamma
        return make_pos_def(to_symmetric(out))
