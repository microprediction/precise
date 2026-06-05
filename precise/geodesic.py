"""Geodesic (Riemannian) exponentially weighted online covariance.

Where :class:`~precise.ewa.EwaCovariance` blends the running estimate with each new
observation by a *Euclidean* convex combination, ``GeodesicEwaCovariance`` instead steps a
fraction ``r`` along the **affine-invariant Riemannian geodesic** on the manifold of
positive-definite matrices, from the current estimate towards the (regularized) rank-one
outer product of the new observation. The result is positive-definite by construction and
respects the curved geometry of covariance space.

The geodesic step (:func:`precise._linalg.geodesic_step`) is reimplemented from
``randomcov.covutil.geodesicinterpolation`` (microprediction/randomcov), so this estimator
carries no dependency beyond numpy.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import geodesic_step
from precise._state import emp_update, ewa_init
from precise.base import BaseOnlineCovariance


class GeodesicEwaCovariance(BaseOnlineCovariance):
    """Recency-weighted covariance that updates along the SPD-manifold geodesic.

    :param r:     Fraction of the geodesic step towards each new observation, in (0, 1].
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, diff: bool = False):
        self.r = r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return ewa_init(n_dim, self.r)

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        # Empirical burn-in to reach a well-conditioned starting point.
        if s["n_samples"] < s["n_burn"]:
            out = emp_update(s, x)
            out["r"] = s["r"]
            out["n_burn"] = s["n_burn"]
            return out
        r = s["r"]
        delta = x - s["mean"]
        mean = (1 - r) * s["mean"] + r * x
        rank_one = np.outer(delta, delta)
        cov = geodesic_step(s["cov"], rank_one, r)
        return {
            "n_dim": s["n_dim"],
            "n_samples": s["n_samples"] + 1,
            "mean": mean,
            "cov": cov,
            "r": r,
            "n_burn": s["n_burn"],
        }
