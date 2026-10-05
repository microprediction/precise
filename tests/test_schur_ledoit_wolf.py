"""Tests specific to SchurLedoitWolfCovariance (the analytic cross-block damping).

The estimator contract (partial_fit, fitted attributes, fit==stream, state roundtrip) is
already exercised by the parametrized suite in test_estimators.py, since the class is in
the registry. Here we check the behaviour that is special to it: the data-estimated
damping gamma_ is a valid reliability that tracks the coupling.
"""
from __future__ import annotations

import numpy as np

from precise import SchurLedoitWolfCovariance, all_estimators


def _block_data(n, p=12, n_blocks=3, within=0.7, cross=0.2, seed=0):
    rng = np.random.default_rng(seed)
    g = np.arange(p) // (p // n_blocks)
    C = cross + (within - cross) * (g[:, None] == g[None, :])
    np.fill_diagonal(C, 1.0)
    return rng.standard_normal((n, p)) @ np.linalg.cholesky(C).T


def test_registered():
    assert SchurLedoitWolfCovariance in all_estimators()


def test_gamma_in_unit_interval_and_pd():
    e = SchurLedoitWolfCovariance(n_blocks=3, r=0.02)
    e.partial_fit(_block_data(500))
    C = e.covariance_
    assert 0.0 <= e.gamma_ <= 1.0
    assert np.all(np.linalg.eigvalsh(C) > 0)


def _gamma(cross, r=0.02, n=2000):
    e = SchurLedoitWolfCovariance(n_blocks=3, r=r)
    e.partial_fit(_block_data(n, within=0.7, cross=cross, seed=1))
    _ = e.covariance_
    return e.gamma_


def test_gamma_rises_with_coupling_strength():
    # stronger true cross-block coupling => higher reliability => larger gamma_
    # (the right invariant for an EWA estimator, whose effective sample is ~1/r, not n)
    g = [_gamma(c) for c in (0.0, 0.1, 0.3, 0.6)]
    assert g[0] < g[1] < g[2] < g[3]


def test_gamma_rises_as_decay_shrinks():
    # smaller r => larger effective sample => the coupling is more reliably estimated
    assert _gamma(0.5, r=0.05) < _gamma(0.5, r=0.005)


def test_gamma_low_when_coupling_is_noise():
    # independent columns => no reliable cross-block coupling => heavy damping (small gamma_)
    rng = np.random.default_rng(2)
    e = SchurLedoitWolfCovariance(n_blocks=3, r=0.02)
    e.partial_fit(rng.standard_normal((2000, 12)))
    _ = e.covariance_
    assert e.gamma_ < 0.5


def test_cross_block_sampling_variance_is_calibrated():
    # The damping is gamma = 1 - b2 / m2, where b2 estimates the sampling variance of the EWA
    # cross-block covariance. It was r * pi_cross, but pi_cross is a prequential dispersion that
    # already contains that sampling variance, so b2 came out twice the truth and gamma was too
    # small (0.20 against 0.60 at correlation 0.2, r=0.05). For the stationary recursion
    # Var(s) = (r/2) E[pi]. Compare b2 with the variance of the final estimate across many
    # independent paths. (#95)
    rng = np.random.default_rng(1)
    r, rho, paths, steps = 0.1, 0.2, 1000, 120
    final, b2 = [], []
    for _ in range(paths):
        z = rng.standard_normal((steps, 2))
        x = np.c_[z[:, 0], rho * z[:, 0] + np.sqrt(1 - rho**2) * z[:, 1]]
        state = SchurLedoitWolfCovariance(r=r, n_blocks=2).fit(x)._state
        final.append(state["cov"][0, 1])
        b2.append(SchurLedoitWolfCovariance._cross_sampling_variance(state) / 2)  # two entries
    ratio = np.mean(b2) / np.var(final)
    assert 0.8 < ratio < 1.25, f"estimated / actual sampling variance = {ratio:.3f}"
