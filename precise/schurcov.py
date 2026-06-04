"""Schur-style online covariance: shrink the cross-block coupling.

A recency-weighted (EWA) covariance whose *cross-block* entries are shrunk by ``gamma`` before use,
with the within-block structure left intact — the estimator-side counterpart of the Schur
complement coupling control that interpolates HRP (``gamma=0``, block-diagonal) and full
optimization (``gamma=1``). It targets the high-dimensional regime where trusting the full inverse
is fragile: damping the (least identifiable) cross-block correlations yields a better-conditioned,
more robust estimate. numpy only.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import geodesic_step, make_pos_def, to_symmetric
from precise._state import ewa_init, ewa_update
from precise.base import BaseOnlineCovariance


class SchurCovariance(BaseOnlineCovariance):
    """Online EWA covariance with Schur-style cross-block coupling shrinkage.

    :param r:             Decay rate of the underlying EWA covariance, in (0, 1].
    :param n_blocks:      Number of contiguous blocks to partition the variables into.
    :param gamma:         Cross-block shrinkage in [0, 1] (0 = block-diagonal, 1 = full covariance).
    :param interpolation: ``"linear"`` (damp cross-block entries by gamma) or ``"geodesic"``
                          (interpolate block-diagonal → full along the affine-invariant SPD geodesic,
                          which stays well-conditioned even when the coupling is strong).
    :param diff:          If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, n_blocks: int = 4, gamma: float = 0.5,
                 interpolation: str = "linear", diff: bool = False):
        self.r = r
        self.n_blocks = n_blocks
        self.gamma = gamma
        self.interpolation = interpolation
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return ewa_init(n_dim, self.r)

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        return ewa_update(s, x)

    def _state_to_cov(self, state: dict) -> np.ndarray:
        cov = np.asarray(state["cov"], dtype=float)
        p = state["n_dim"]
        nb = min(self.n_blocks, p)
        block_id = np.empty(p, dtype=int)
        for bi, idx in enumerate(np.array_split(np.arange(p), nb)):
            block_id[idx] = bi
        cross = block_id[:, None] != block_id[None, :]
        if self.interpolation == "geodesic":
            block_diag = cov.copy()
            block_diag[cross] = 0.0
            return geodesic_step(make_pos_def(block_diag), make_pos_def(cov), self.gamma)
        out = cov.copy()
        out[cross] *= self.gamma
        return make_pos_def(to_symmetric(out))
