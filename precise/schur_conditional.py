"""Online Schur covariance from damped, ridge-regressed block conditionals.

Where :class:`SchurLedoitWolfCovariance` shrinks the cross-block *entries* elementwise (an
inversion-free operation), this estimator damps the *structured* Schur factorization: for each
block ``k`` it forms the conditional regression (hedge) ``b_k`` and Schur complement ``S_k``,
damps both by the cross-block coupling reliability ``gamma*``, and reassembles the implied
positive-definite covariance. The hedge ``b_k`` is computed through a *ridge-regularized*
inverse of the conditioning block, so the structured operation does not inherit the unstable
``R_cc^{-1}`` that makes a raw block-conditional estimate blow up when ``n < p`` -- the same
regularization the allocation side applies to a hedge. ``gamma*`` is the Gaussian (OAS-style)
cross-block coupling reliability, estimated from the data with no tuning: small when the coupling
is dominated by sampling noise, tending to ``1`` as it becomes well estimated.

At ``gamma_ -> 0`` the estimate is block-diagonal; with ``n_blocks=1`` it is the full EWA
covariance. This is the structured (Vecchia/conditional) counterpart of the entry-shrinkage
:class:`SchurLedoitWolfCovariance`; both set the damping by the coupling reliability. numpy only.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import cov_to_corrcoef, make_pos_def, to_symmetric
from precise._state import ewa_init, ewa_update
from precise.base import BaseOnlineCovariance


class SchurConditionalCovariance(BaseOnlineCovariance):
    """Online Schur covariance from damped, ridge-regressed block conditionals.

    :param r:         Decay rate of the underlying EWA covariance, in (0, 1].
    :param n_blocks:  Number of contiguous blocks to partition the variables into.
    :param diff:      If ``True``, estimate the covariance of first differences of the stream.

    After fitting, the data-estimated cross-block damping is available as ``self.gamma_`` (it is
    populated when ``covariance_``/``correlation_``/``precision_`` is read).
    """

    def __init__(self, r: float = 0.05, n_blocks: int = 4, diff: bool = False):
        self.r = r
        self.n_blocks = n_blocks
        self.diff = diff
        self.gamma_: float | None = None
        super().__init__()

    def _slices(self, p: int) -> list[tuple[int, int]]:
        nb = min(max(1, self.n_blocks), p)
        return [(int(idx[0]), int(idx[-1]) + 1) for idx in np.array_split(np.arange(p), nb)]

    def _block_id(self, p: int) -> np.ndarray:
        nb = min(max(1, self.n_blocks), p)
        bid = np.empty(p, dtype=int)
        for bi, idx in enumerate(np.array_split(np.arange(p), nb)):
            bid[idx] = bi
        return bid

    def _init_state(self, n_dim: int) -> dict:
        return ewa_init(n_dim, self.r)

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        return ewa_update(s, x)

    def _n_eff(self, state: dict) -> float:
        # Effective sample size: the empirical count during burn-in, the EWA window thereafter.
        r = float(state["r"])
        return max(2.0, min(float(state["n_samples"]), (2.0 - r) / r))

    def _gamma_star(self, R: np.ndarray, n_eff: float) -> float:
        """Gaussian (OAS-style) cross-block coupling reliability: how much of the estimated
        cross-block correlation to keep, given its finite-sample variance ``(1+r^2)/n_eff``."""
        bid = self._block_id(R.shape[0])
        cross = bid[:, None] != bid[None, :]
        rij = R[cross]
        if rij.size == 0:
            return 1.0
        var_g = (1.0 + rij ** 2) / n_eff
        num = float(np.clip(rij ** 2 - var_g, 0.0, None).sum())
        den = float((rij ** 2).sum())
        return float(np.clip(num / den, 0.0, 1.0)) if den > 0 else 0.0

    def _state_to_cov(self, state: dict) -> np.ndarray:
        cov = np.asarray(state["cov"], dtype=float)
        p = cov.shape[0]
        sl = self._slices(p)
        d = np.sqrt(np.clip(np.diag(cov), 1e-12, None))
        R = cov_to_corrcoef(cov)
        n_eff = self._n_eff(state)
        gamma = self._gamma_star(R, n_eff)
        self.gamma_ = gamma
        # Structured, ridge-regressed Schur reassembly into an implied positive-definite matrix.
        Rg = np.zeros((p, p))
        a0, b0 = sl[0]
        Rg[a0:b0, a0:b0] = R[a0:b0, a0:b0]
        for k in range(1, len(sl)):
            ak, bk = sl[k]
            pa, pb = 0, ak                          # condition on all previous variables
            Rcc = R[pa:pb, pa:pb]
            ridge = float(np.clip((pb - pa) / n_eff, 0.0, 0.9))  # ~ conditioning_dim / n_eff
            Rcc_reg = (1.0 - ridge) * Rcc + ridge * np.diag(np.diag(Rcc))
            Rck = R[pa:pb, ak:bk]
            Rkk = R[ak:bk, ak:bk]
            b = np.linalg.solve(Rcc_reg + 1e-10 * np.eye(pb - pa), Rck)   # robust (ridge) hedge
            S = make_pos_def(to_symmetric(Rkk - Rck.T @ b))              # conditional covariance
            bg = gamma * b
            Sg = (1.0 - gamma) * Rkk + gamma * S
            Rprev = Rg[pa:pb, pa:pb]
            Rg[ak:bk, pa:pb] = bg.T @ Rprev
            Rg[pa:pb, ak:bk] = Rg[ak:bk, pa:pb].T
            Rg[ak:bk, ak:bk] = Sg + bg.T @ Rprev @ bg
        Rg = make_pos_def(to_symmetric(Rg))
        return Rg * np.outer(d, d)                                       # back to covariance
