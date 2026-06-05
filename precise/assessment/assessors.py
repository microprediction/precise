"""Concrete covariance-estimate assessors (higher score == better).

Spans the families surveyed in ``papers/evaluation_and_generation_review.md``: a proper log score,
a Schur-style block pseudo-likelihood, decision-theoretic Stein loss, a matrix loss to the truth,
an economic (minimum-variance) criterion, and an inversion-free proper scoring rule (variogram).
numpy only.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import geodesic_step, make_pos_def, to_symmetric, try_invert
from precise.assessment.base import Assessor

_LOG2PI = np.log(2 * np.pi)


def _gaussian_loglik(cov: np.ndarray, X: np.ndarray) -> float:
    prec = try_invert(cov)
    _, logdet = np.linalg.slogdet(prec)
    quad = np.einsum("ij,jk,ik->i", X, prec, X)
    return float(np.mean(0.5 * logdet - 0.5 * quad - 0.5 * cov.shape[0] * _LOG2PI))


class LogLikelihood(Assessor):
    """Held-out Gaussian log-likelihood — the logarithmic (strictly proper) score.

    Most powerful when the precision is trustworthy (Neyman-Pearson); fragile in high dimensions.
    """

    def score(self, cov, *, X_test=None, true_cov=None) -> float:
        return _gaussian_loglik(np.asarray(cov, dtype=float), X_test)


class BlockPseudoLikelihood(Assessor):
    """Schur-style block (composite) pseudo-likelihood: sum of log-likelihoods on small blocks.

    Inverts only ``block_size`` x ``block_size`` matrices — cheap and robust in high dimensions
    (the evaluation analogue of the HRP/Schur allocation principle). ``block_size`` is the
    robustness<->power knob; a block of the full dimension recovers the full likelihood.
    """

    def __init__(self, block_size: int = 10):
        self.block_size = block_size

    def score(self, cov, *, X_test=None, true_cov=None) -> float:
        cov = np.asarray(cov, dtype=float)
        p = len(cov)
        total = 0.0
        for s in range(0, p, self.block_size):
            idx = slice(s, min(s + self.block_size, p))
            total += _gaussian_loglik(cov[idx, idx], X_test[:, idx])
        return total

    def __repr__(self):
        return f"BlockPseudoLikelihood(block_size={self.block_size})"


class SchurLikelihood(Assessor):
    """The γ-regularized Schur likelihood — a tunable bridge between the full and block-diagonal
    likelihoods.

    Partition the variables into ``n_blocks`` contiguous blocks and interpolate the covariance
    between its block-diagonal part (γ=0) and the full matrix (γ=1) by damping the cross-block
    coupling — i.e. the Schur complement — then score the Gaussian likelihood. ``γ`` is a
    *coupling-strength* knob: γ→1 recovers the full likelihood (most powerful, fragile in high
    dimensions), γ→0 the block-diagonal likelihood (robust), and an interior γ can beat *both* when
    the coupling is only partially reliable — the evaluation mirror of Schur complementary
    allocation (HRP ↔ minimum variance).

    ``interpolation="linear"`` damps the cross-block covariance by γ; ``"geodesic"`` interpolates
    along the affine-invariant SPD geodesic (lifting small eigenvalues multiplicatively).

    Grounded in the same exact Schur-complement conditioning identity as the Vecchia / Gaussian-
    Markov-random-field likelihoods (γ=1 is a block-Vecchia / GMRF likelihood); those regularize by
    *sparsity* (which to condition on), whereas γ adds an orthogonal coupling-*strength* axis.
    """

    def __init__(self, gamma: float = 0.5, n_blocks: int = 4, interpolation: str = "linear"):
        self.gamma = gamma
        self.n_blocks = n_blocks
        self.interpolation = interpolation

    def score(self, cov, *, X_test=None, true_cov=None) -> float:
        cov = np.asarray(cov, dtype=float)
        p = len(cov)
        nb = min(self.n_blocks, p)
        block_id = np.empty(p, dtype=int)
        for bi, idx in enumerate(np.array_split(np.arange(p), nb)):
            block_id[idx] = bi
        cross = block_id[:, None] != block_id[None, :]
        if self.interpolation == "geodesic":
            block_diag = cov.copy()
            block_diag[cross] = 0.0
            cov_gamma = geodesic_step(make_pos_def(block_diag), make_pos_def(cov), self.gamma)
        else:
            cov_gamma = cov.copy()
            cov_gamma[cross] *= self.gamma
        return _gaussian_loglik(make_pos_def(cov_gamma), X_test)

    def __repr__(self):
        return (
            f"SchurLikelihood(gamma={self.gamma}, n_blocks={self.n_blocks}, "
            f"interpolation={self.interpolation!r})"
        )


class SteinLoss(Assessor):
    """Negative Stein (entropy) loss against the held-out sample covariance.

    ``-(tr(M) - logdet(M) - p)`` with ``M = cov^{-1} S``; the natural decision-theoretic covariance
    loss (= KL to the sample covariance). Inverts the estimate, so it shares the high-dim fragility.
    """

    def score(self, cov, *, X_test=None, true_cov=None) -> float:
        cov = np.asarray(cov, dtype=float)
        S = np.cov(X_test, rowvar=False, bias=True)
        M = try_invert(cov) @ np.atleast_2d(S)
        _, logdet = np.linalg.slogdet(M)
        return -float(np.trace(M) - logdet - len(cov))


class FrobeniusToTruth(Assessor):
    """Negative relative Frobenius distance to the true covariance (truth-based, synthetic only).

    Never inverts, so it is robust in high dimensions; but scale-dominated and blind to differences
    in correlation/precision structure that do not move the large entries.
    """

    needs_data = False
    needs_truth = True

    def score(self, cov, *, X_test=None, true_cov=None) -> float:
        cov = np.asarray(cov, dtype=float)
        true_cov = np.asarray(true_cov, dtype=float)
        return -float(np.linalg.norm(cov - true_cov) / np.linalg.norm(true_cov))


class GMVVariance(Assessor):
    """Negative out-of-sample variance of the global-minimum-variance portfolio ``w ∝ cov^{-1} 1``.

    The dominant economic criterion (Ledoit-Wolf; Engle-Ledoit-Wolf). Precision-sensitive, so it
    fails like the likelihood when the inverse is untrustworthy — the bridge to portfolio theory.
    """

    def score(self, cov, *, X_test=None, true_cov=None) -> float:
        cov = np.asarray(cov, dtype=float)
        w = try_invert(cov) @ np.ones(len(cov))
        w = w / w.sum()
        return -float(np.mean((X_test @ w) ** 2))


class VariogramScore(Assessor):
    """Negative (order-1) variogram score — a proper scoring rule that never inverts the covariance.

    Compares observed pairwise absolute differences to their Gaussian expectations
    ``E|Y_i - Y_j| = sqrt(2/pi (cov_ii + cov_jj - 2 cov_ij))``. Inversion-free, hence robust in high
    dimensions (Scheuerer & Hamill 2015).
    """

    def score(self, cov, *, X_test=None, true_cov=None) -> float:
        cov = to_symmetric(np.asarray(cov, dtype=float))
        d = np.diag(cov)
        expected = np.sqrt(np.maximum(d[:, None] + d[None, :] - 2 * cov, 0.0) * (2.0 / np.pi))
        X = np.atleast_2d(X_test)
        # mean over samples of sum_{i,j} (|x_i - x_j| - expected_ij)^2
        diffs = np.abs(X[:, :, None] - X[:, None, :])  # (n, p, p)
        return -float(np.mean(np.sum((diffs - expected[None]) ** 2, axis=(1, 2))))
