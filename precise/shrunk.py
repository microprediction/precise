"""Fixed-intensity shrinkage covariance, towards identity or a constant-correlation target.

Where :class:`~precise.ledoitwolf.LedoitWolfCovariance` and :class:`~precise.oas.OASCovariance`
estimate the shrinkage intensity from the data, ``ShrunkCovariance`` uses a fixed intensity
``delta`` (transparent and predictable, mirroring ``sklearn.covariance.ShrunkCovariance``) and
offers a choice of target. The **constant-correlation** target — every pair shrunk towards the
average sample correlation — is the finance-relevant one (assets share a positive baseline
correlation), versus the scaled-identity target that pulls towards zero correlation.
"""

from __future__ import annotations

import numpy as np

from precise._state import ewa_init, ewa_update
from precise.base import BaseOnlineCovariance


class ShrunkCovariance(BaseOnlineCovariance):
    """Online exponentially weighted covariance with fixed-intensity shrinkage.

    :param r:       Decay rate of the underlying EWA covariance, in (0, 1].
    :param delta:   Shrinkage intensity in [0, 1] (0 = no shrinkage, 1 = the target).
    :param target:  ``"constant_correlation"`` (default) or ``"identity"``.
    :param diff:    If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(
        self,
        r: float = 0.05,
        delta: float = 0.1,
        target: str = "constant_correlation",
        diff: bool = False,
    ):
        self.r = r
        self.delta = delta
        self.target = target
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return ewa_init(n_dim, self.r)

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        return ewa_update(s, x)

    def _state_to_cov(self, state: dict) -> np.ndarray:
        S = np.asarray(state["cov"], dtype=float)
        p = state["n_dim"]
        if self.target == "identity":
            target = (np.trace(S) / p) * np.eye(p)
        else:  # constant_correlation
            d = np.sqrt(np.maximum(np.diag(S), 1e-12))
            corr = S / np.outer(d, d)
            off = corr[~np.eye(p, dtype=bool)]
            rbar = float(np.mean(off)) if off.size else 0.0
            target = rbar * np.outer(d, d)
            np.fill_diagonal(target, np.diag(S))  # preserve the variances
        return (1.0 - self.delta) * S + self.delta * target
