"""Online Oracle Approximating Shrinkage (OAS) covariance.

Like :class:`~precise.ledoitwolf.LedoitWolfCovariance`, OAS shrinks an exponentially weighted
sample covariance towards a scaled identity, but uses the Chen, Wiesel, Eldar & Hero (2010)
shrinkage intensity, which is often better conditioned for Gaussian data. The intensity is a pure
function of the running covariance, so it is applied lazily on read; the per-step update is just an
EWA covariance update (O(d^2), no stored window). ``sklearn`` only ships the batch version.
"""

from __future__ import annotations

import numpy as np

from precise._state import ewa_init, ewa_update
from precise.base import BaseOnlineCovariance


class OASCovariance(BaseOnlineCovariance):
    """Online OAS shrinkage covariance.

    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
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

    def _state_to_cov(self, state: dict) -> np.ndarray:
        S = np.asarray(state["cov"], dtype=float)
        p = state["n_dim"]
        # Effective sample size of the exponentially weighted estimator.
        n = max(1.0 / state["r"], 2.0)
        tr = np.trace(S)
        tr2 = np.trace(S @ S)
        mu = tr / p
        num = (1.0 - 2.0 / p) * tr2 + tr * tr
        den = (n + 1.0 - 2.0 / p) * (tr2 - tr * tr / p)
        rho = 1.0 if den <= 0 else min(max(num / den, 0.0), 1.0)
        return (1.0 - rho) * S + rho * mu * np.eye(p)
