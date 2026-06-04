"""Linear-algebra helpers acting on covariance / correlation / precision matrices.

Numpy only. Ported and trimmed from the previous ``covarianceutil.covfunctions``
(the pandas/DataFrame branches and portfolio/Schur helpers were dropped — those
live in the ``schur`` package now). ``geodesic_step`` is new; it is a reimplementation
of the affine-invariant SPD geodesic from ``randomcov.covutil.geodesicinterpolation``
(credit: microprediction/randomcov) so that the geometric estimator carries no
dependency beyond numpy.
"""

from __future__ import annotations

import numpy as np

EPS = 1e-12


def is_symmetric(a: np.ndarray, rtol: float = 1e-05, atol: float = 1e-08) -> bool:
    return bool(np.allclose(a, a.T, rtol=rtol, atol=atol))


def to_symmetric(a: np.ndarray) -> np.ndarray:
    return (a + a.T) / 2.0


def cov_to_corrcoef(a: np.ndarray) -> np.ndarray:
    """Normalize a covariance matrix to a correlation matrix (unit diagonal)."""
    variances = np.diagonal(a)
    denominator = np.sqrt(variances[np.newaxis, :] * variances[:, np.newaxis]) + EPS
    return a / denominator


def is_positive_def(a: np.ndarray) -> bool:
    """True when ``a`` is positive-definite, tested via Cholesky."""
    try:
        np.linalg.cholesky(a)
        return True
    except np.linalg.LinAlgError:
        return False


def nearest_pos_def(a: np.ndarray) -> np.ndarray:
    """Nearest positive-definite matrix to ``a``.

    A numpy port of John D'Errico's ``nearestSPD`` MATLAB code, after Higham (1988).
    """
    b = to_symmetric(a)
    _, s, V = np.linalg.svd(b)
    H = V.T @ np.diag(s) @ V
    a3 = to_symmetric((b + H) / 2)
    if is_positive_def(a3):
        return a3

    spacing = np.spacing(np.linalg.norm(a))
    identity = np.eye(a.shape[0])
    k = 1
    while not is_positive_def(a3):
        mineig = np.min(np.real(np.linalg.eigvals(a3)))
        a3 += identity * (-mineig * k**2 + spacing)
        k += 1
    return a3


def make_pos_def(a: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """Cheap symmetrize-and-floor: clip eigenvalues up to ``eps``. Always SPD."""
    a = to_symmetric(a)
    evals, evecs = np.linalg.eigh(a)
    evals = np.clip(evals, eps, None)
    return to_symmetric((evecs * evals) @ evecs.T)


def affine_shrink(a: np.ndarray, phi: float = 1.01, lmbd: float = 0.01) -> np.ndarray:
    """Ridge the diagonal (``phi``) then shrink towards the grand-mean diagonal (``lmbd``)."""
    n = a.shape[0]
    b = np.copy(a)
    idx = np.diag_indices(n)
    b[idx] = b[idx] * phi
    mu = np.mean(np.diag(b))
    return (1 - lmbd) * b + lmbd * mu * np.eye(n)


def try_invert(a: np.ndarray, phi: float = 1.01, lmbd: float = 0.01) -> np.ndarray:
    """Invert a matrix, falling back to pseudo-inverse then ridge+shrinkage."""
    try:
        return np.linalg.inv(a)
    except np.linalg.LinAlgError:
        try:
            return np.linalg.pinv(a)
        except np.linalg.LinAlgError:
            return np.linalg.inv(affine_shrink(a, phi=phi, lmbd=lmbd))


def weaken_cov(
    cov: np.ndarray,
    diag_multipliers,
    off_diag_additional_factor: float = 0.9,
) -> np.ndarray:
    """Shrink a covariance matrix by scaling diagonal and off-diagonal entries.

    Kept as a reusable shrink primitive (the portfolio-motivated *stopping criterion*
    that used to drive it lives in the ``schur`` package).
    """
    covs = np.copy(cov)
    diag_multipliers = np.asarray(diag_multipliers, dtype=float)
    n = covs.shape[0]
    for i in range(n):
        covs[i, i] *= diag_multipliers[i]
        for j in range(n):
            if j != i:
                covs[i, j] *= off_diag_additional_factor * np.sqrt(
                    diag_multipliers[i] * diag_multipliers[j]
                )
    return covs


def geodesic_step(start: np.ndarray, end: np.ndarray, gamma: float) -> np.ndarray:
    """Move a fraction ``gamma`` along the affine-invariant Riemannian geodesic.

    Interpolates between two SPD matrices ``start`` and ``end`` on the manifold of
    positive-definite matrices: ``gamma=0`` returns ``start``, ``gamma=1`` returns
    ``end``. The result is SPD by construction.

    Reimplemented (eigh-based, numpy only) from
    ``randomcov.covutil.geodesicinterpolation.geodesic_interpolation``.
    """
    start = make_pos_def(start)
    end = make_pos_def(end)

    evals_s, evecs_s = np.linalg.eigh(start)
    evals_s = np.clip(evals_s, EPS, None)
    start_sqrt = (evecs_s * np.sqrt(evals_s)) @ evecs_s.T
    start_inv_sqrt = (evecs_s * (1.0 / np.sqrt(evals_s))) @ evecs_s.T

    middle = to_symmetric(start_inv_sqrt @ end @ start_inv_sqrt)
    evals_m, evecs_m = np.linalg.eigh(middle)
    evals_m = np.clip(evals_m, 0.0, None) ** gamma
    middle_power = (evecs_m * evals_m) @ evecs_m.T

    return to_symmetric(start_sqrt @ middle_power @ start_sqrt)
