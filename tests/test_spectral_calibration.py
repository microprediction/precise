"""Smoke test and correctness checks for the (non-shipped) online spectral calibration research."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

sc = pytest.importorskip("research.spectral_calibration")


def test_frobenius_identity_that_motivates_the_objective():
    # || U diag(d) U' - x x' ||_F^2 == sum_i (d_i - z_i^2)^2 + (a term free of d).
    # This is the whole justification for training on squared projections, so pin it: the
    # residual must be *constant* in d, not merely small.
    rng = np.random.default_rng(0)
    p = 7
    U = np.linalg.qr(rng.standard_normal((p, p)))[0]
    x = rng.standard_normal(p)
    z = U.T @ x
    residuals = []
    for _ in range(5):
        d = np.abs(rng.standard_normal(p)) + 0.1
        total = np.sum((U @ np.diag(d) @ U.T - np.outer(x, x)) ** 2)
        residuals.append(total - np.sum((d - z**2) ** 2))
    assert np.allclose(residuals, residuals[0], atol=1e-8)
    assert np.isclose(residuals[0], np.sum(np.outer(z**2, z**2)) - np.sum(z**4), atol=1e-8)


def test_labels_are_conditionally_unbiased():
    # E[z_i^2 | past] = u_i' Sigma u_i -- the identity the learner relies on. Averaging squared
    # projections onto a *fixed* basis must recover the Rayleigh quotients of the true covariance.
    rng = np.random.default_rng(1)
    p = 5
    A = rng.standard_normal((p, p))
    cov = A @ A.T + np.eye(p)
    U = np.linalg.qr(rng.standard_normal((p, p)))[0]
    X = rng.multivariate_normal(np.zeros(p), cov, size=200_000)
    assert np.allclose(np.mean((X @ U) ** 2, axis=0), np.diag(U.T @ cov @ U), rtol=0.05)


@pytest.mark.parametrize("mode", ["rank", "eigenvalue", "shared"])
def test_estimator_is_psd_and_tracks_a_stationary_covariance(mode):
    rng = np.random.default_rng(2)
    p = 8
    A = rng.standard_normal((p, p))
    cov = A @ A.T + np.eye(p)
    chol = np.linalg.cholesky(cov)
    est = sc.CalibratedSpectrumCovariance(r=0.02, refresh=10, mode=mode)
    for _ in range(2000):
        est.partial_fit(chol @ rng.standard_normal(p))
    C = est.covariance_
    assert C.shape == (p, p)
    assert np.allclose(C, C.T, atol=1e-8)
    assert np.linalg.eigvalsh(C).min() > 0, "the kernel map is a ratio of positive accumulators"
    assert np.sum((C - cov) ** 2) / np.sum(cov**2) < 0.25


def test_rayleigh_recursion_matches_an_explicit_eigendecomposition():
    # Between refreshes the eigenvalues are tracked as (1-r)*lam + r*z^2 rather than recomputed.
    # For a fixed basis that must agree with the quadratic form of the accumulated covariance.
    rng = np.random.default_rng(3)
    p = 6
    est = sc.CalibratedSpectrumCovariance(r=0.02, refresh=10_000)
    X = rng.standard_normal((400, p))
    for x in X:
        est.partial_fit(x)
    explicit = np.diag(est._basis.T @ est._cov @ est._basis)
    assert np.allclose(est._lam, explicit, rtol=1e-6, atol=1e-8)


def test_run_and_report_cover_every_scenario():
    results = sc.run(p=8, n=300, seeds=1, burn=100, every=50)
    assert set(results) == set(sc.scenarios(8, 300, np.random.default_rng(0)))
    for cells in results.values():
        assert "shared calib" in cells and "Raw EW" in cells
        assert all(np.isfinite(v) and v >= 0 for v in cells.values())
    assert "scenario" in sc.report(results)
