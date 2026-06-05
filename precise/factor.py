"""Online low-rank-plus-diagonal (approximate factor) covariance.

Maintains the top-``k`` principal directions incrementally with CCIPCA (Weng, Zhang & Hwang,
2003) plus a per-coordinate residual variance, so the covariance is represented as
``V Λ Vᵀ + diag(ψ)``. The per-step update is **O(d·k)** rather than O(d²), which is what makes a
streaming covariance feasible when ``d`` is large (hundreds–thousands of variables). The full dense
matrix is only materialized when you read ``covariance_``.
"""

from __future__ import annotations

import numpy as np

from precise.base import BaseOnlineCovariance


class FactorCovariance(BaseOnlineCovariance):
    """Online approximate factor-model covariance (low rank + diagonal residual).

    :param k:     Number of factors (principal directions) to track.
    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, k: int = 2, r: float = 0.05, diff: bool = False):
        self.k = k
        self.r = r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        k = min(self.k, n_dim)
        return {
            "n_dim": n_dim,
            "n_samples": 0,
            "mean": np.zeros(n_dim),
            "var": np.zeros(n_dim),  # per-coordinate total variance
            "V": np.zeros((k, n_dim)),  # CCIPCA eigen-estimates (norm == eigenvalue)
            "k": k,
            "r": float(self.r),
            "n_burn": k + 1,
        }

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        n = s["n_samples"] + 1
        r, k, n_burn = s["r"], s["k"], s["n_burn"]

        dev = x - s["mean"]
        sq = dev * dev
        if n <= n_burn:
            # Sample-mean learning rate / empirical accumulation while warming up.
            lr = 1.0 / n
            mean = s["mean"] + (x - s["mean"]) / n
            var = s["var"] + (sq - s["var"]) / n
        else:
            lr = r
            mean = (1 - r) * s["mean"] + r * x
            var = (1 - r) * s["var"] + r * sq

        V = np.array(s["V"], dtype=float)
        u = dev.copy()
        for j in range(k):
            norm = np.linalg.norm(V[j])
            if norm < 1e-12:
                V[j] = u  # seed an empty component, one per early step
                break
            vhat = V[j] / norm
            proj = float(u @ vhat)
            V[j] = (1 - lr) * V[j] + lr * proj * u
            u = u - proj * vhat  # deflate so the next component finds the next direction

        return {
            "n_dim": s["n_dim"],
            "n_samples": n,
            "mean": mean,
            "var": var,
            "V": V,
            "k": k,
            "r": r,
            "n_burn": n_burn,
        }

    def _state_to_cov(self, state: dict) -> np.ndarray:
        V = np.asarray(state["V"], dtype=float)
        p = state["n_dim"]
        factor = np.zeros((p, p))
        captured = np.zeros(p)
        for vj in V:
            norm = np.linalg.norm(vj)
            if norm > 1e-12:
                factor += np.outer(vj, vj) / norm  # = lambda * vhat vhatᵀ  (since ||vj|| == lambda)
                captured += norm * (vj / norm) ** 2
        # Idiosyncratic residual makes the diagonal match the tracked total variance.
        resid = np.maximum(np.asarray(state["var"], dtype=float) - captured, 0.0)
        return factor + np.diag(resid)
