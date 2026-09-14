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


def to_symmetric(a: np.ndarray) -> np.ndarray:
    return (a + a.T) / 2.0


def cov_to_corrcoef(a: np.ndarray) -> np.ndarray:
    """Normalize a covariance matrix to a correlation matrix (unit diagonal).

    The guard against a zero variance is relative, not additive. ``sqrt(v_i v_j) + EPS`` adds a
    constant with units of variance to a quantity with units of variance, so it stops being
    negligible exactly when the data is small: at variances of 1e-12 the additive 1e-12 halved
    every entry, and the diagonal -- which is one by definition -- came back as 0.5. At 1e-13 it
    came back as 0.09, and a true correlation of 0.5 read as 0.045.

    Flooring each variance at a fraction of the largest keeps the unit diagonal at every scale and
    still avoids dividing by a genuinely zero variance.
    """
    variances = np.asarray(np.diagonal(a), dtype=float)
    largest = float(variances.max()) if variances.size else 0.0
    floor = EPS * largest if largest > 0.0 else EPS
    safe = np.clip(variances, floor, None)
    denominator = np.sqrt(safe[np.newaxis, :] * safe[:, np.newaxis])
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
    """Cheap symmetrize-and-floor: clip eigenvalues up to ``eps`` times the largest. Always SPD.

    The floor is *relative*. An absolute one has units of variance, so it silently decides the
    answer whenever the data is small: at a data scale of 1e-6 the true variances are around
    1e-12, every eigenvalue is below an absolute 1e-8, and this returned ``1e-8 * I`` -- an
    estimate up to nine thousand times too large that carries no correlation information at all.
    Block, Schur, SchurLedoitWolf and Geodesic all did exactly that.

    Worse in one case. GeodesicEwaCovariance interpolates toward ``np.outer(delta, delta)``, whose
    other ``p - 1`` eigenvalues are zero and were floored here to 1e-8. Because the rank-one
    direction rotates every step, no direction was ever sustained and the estimate collapsed onto
    the floor: measured, a true trace of 9.49 became 2.4e-06 within about forty observations and
    stayed there, giving a variance forecast seven million times too small.

    Relative to the largest eigenvalue, the floor is scale-equivariant: multiply the data by ``c``
    and the estimate multiplies by ``c**2``, as a covariance must. A matrix with no positive
    eigenvalue at all has no scale to be relative to, so it falls back to the absolute value.
    """
    a = to_symmetric(a)
    evals, evecs = np.linalg.eigh(a)
    largest = float(evals[-1]) if evals.size else 0.0
    floor = eps * largest if largest > 0.0 else eps
    evals = np.clip(evals, floor, None)
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
