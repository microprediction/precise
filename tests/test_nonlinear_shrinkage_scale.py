"""The spectrum must not collapse when one variable is much smaller than the rest.

Shipped in 1.1.0 and found by audit. The null-eigenvalue tolerance was scaled by machine epsilon,
which excludes a relative eigenvalue of 1e-15 but admits one of 1e-10 — and the kernel divides by
the eigenvalue, so an admitted near-null contributes ~1/lam to the Hilbert transform of every other
eigenvalue and drives the whole shrunk spectrum to zero. The result is finite, non-negative and
symmetric, so every existing contract test passed on a covariance 1e-9 of the truth.

The band is reachable from ordinary data, not contrived spectra: one series quoted in basis points
among percents, or a hedged pair.
"""

import numpy as np
import pytest

from precise.nonlinear_shrinkage import (
    EwaNonlinearShrinkageCovariance,
    NonlinearShrinkageCovariance,
    WindowedNonlinearShrinkageCovariance,
)

ESTIMATORS = (
    NonlinearShrinkageCovariance,
    WindowedNonlinearShrinkageCovariance,
    EwaNonlinearShrinkageCovariance,
)


def _stream(cls, X):
    est = cls()
    for row in X:
        est.partial_fit(row)
    return est


@pytest.mark.parametrize("cls", ESTIMATORS)
@pytest.mark.parametrize("scale", [1e0, 1e-2, 1e-3, 1e-4, 1e-6, 1e-9, 1e-12])
def test_one_small_variable_does_not_collapse_the_spectrum(cls, scale):
    rng = np.random.default_rng(0)
    X = rng.standard_normal((200, 10))
    X[:, 0] *= scale

    cov = _stream(cls, X).covariance_
    raw = float(np.trace(np.cov(X.T)))
    got = float(np.trace(cov))

    assert np.all(np.isfinite(cov))
    assert 0.5 * raw <= got <= 2.0 * raw, (
        f"{cls.__name__} at scale {scale:g}: trace {got:.3e} against sample {raw:.3e} "
        f"(ratio {got / raw:.2e}) — the spectrum collapsed"
    )


@pytest.mark.parametrize("cls", ESTIMATORS)
@pytest.mark.parametrize("eps", [1e-2, 1e-4, 1e-6, 1e-8])
def test_a_hedged_pair_does_not_collapse_the_spectrum(cls, eps):
    # The case the module docstring cites as the reason rank is measured rather than assumed.
    rng = np.random.default_rng(3)
    X = rng.standard_normal((300, 8))
    X[:, 1] = X[:, 0] + eps * rng.standard_normal(300)

    cov = _stream(cls, X).covariance_
    raw = float(np.trace(np.cov(X.T)))
    got = float(np.trace(cov))

    assert np.all(np.isfinite(cov))
    assert 0.5 * raw <= got <= 2.0 * raw, (
        f"{cls.__name__} at eps {eps:g}: trace ratio {got / raw:.2e} — the spectrum collapsed"
    )


def test_genuinely_null_directions_still_stay_null():
    # The guard must not have been loosened into inventing variance for directions the data
    # does not span. An exactly rank-3 stream in 8 dimensions keeps 5 null eigenvalues.
    rng = np.random.default_rng(11)
    basis = rng.standard_normal((3, 8))
    X = rng.standard_normal((200, 3)) @ basis

    cov = _stream(NonlinearShrinkageCovariance, X).covariance_
    lam = np.sort(np.linalg.eigvalsh(cov))
    assert np.all(lam >= -1e-10)
    assert np.sum(lam > lam[-1] * 1e-6) <= 3, (
        f"rank-3 data produced {np.sum(lam > lam[-1] * 1e-6)} informative directions"
    )
    assert np.trace(cov) > 0.5 * np.trace(np.cov(X.T))
