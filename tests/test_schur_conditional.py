"""Tests for SchurConditionalCovariance: structured Schur damping with a ridge-regressed hedge.

The generic estimator contract is covered by the parametrized suite; here we check what is
special: positive-definiteness, stability at n<p (the raw-OLS version blows up there), the
reliability behaviour of gamma_, the n_blocks=1 reduction, and JSON state roundtrip.
"""
from __future__ import annotations

import json

import numpy as np

from precise import EwaCovariance, SchurConditionalCovariance, all_estimators


def _blocky(n, p=24, n_blocks=4, rho_within=0.7, rho_cross=0.1, seed=0):
    rng = np.random.default_rng(seed)
    bid = np.repeat(np.arange(n_blocks), p // n_blocks)
    C = rho_cross * np.ones((p, p)) + (rho_within - rho_cross) * (bid[:, None] == bid[None, :])
    np.fill_diagonal(C, 1.0)
    L = np.linalg.cholesky(C)
    return rng.standard_normal((n, p)) @ L.T


def test_registered():
    assert SchurConditionalCovariance in all_estimators()


def test_pd_and_symmetric():
    e = SchurConditionalCovariance(n_blocks=4).fit(_blocky(300, p=24))
    C = e.covariance_
    assert np.allclose(C, C.T, atol=1e-10)
    assert np.all(np.linalg.eigvalsh(C) > 0)


def test_stable_when_undersampled():
    # n < p: the raw-OLS structured Schur blows up here; the ridge hedge must stay finite + PD.
    e = SchurConditionalCovariance(n_blocks=4).fit(_blocky(15, p=40))
    C = e.covariance_
    assert np.all(np.isfinite(C))
    assert np.all(np.linalg.eigvalsh(C) > 0)


def test_gamma_in_unit_interval():
    e = SchurConditionalCovariance(n_blocks=4).fit(_blocky(200, p=24))
    _ = e.covariance_
    assert e.gamma_ is not None and 0.0 <= e.gamma_ <= 1.0


def test_gamma_rises_with_coupling_strength():
    # stronger genuine cross-block coupling -> higher kept fraction gamma*
    def g(rc):
        e = SchurConditionalCovariance(n_blocks=4, r=0.02).fit(_blocky(400, p=24, rho_cross=rc))
        _ = e.covariance_
        return e.gamma_
    assert g(0.45) > g(0.02)


def test_n_blocks_one_is_full_ewa():
    X = _blocky(300, p=20)
    C1 = SchurConditionalCovariance(n_blocks=1, r=0.05).fit(X).covariance_
    Cewa = EwaCovariance(r=0.05).fit(X).covariance_
    assert np.allclose(C1, Cewa, atol=1e-8)


def test_state_roundtrips():
    e = SchurConditionalCovariance(n_blocks=4).fit(_blocky(200, p=24))
    state = e.get_state()
    json.loads(json.dumps(state))                                  # JSON-serializable
    restored = SchurConditionalCovariance().set_state(state)
    assert np.allclose(restored.covariance_, e.covariance_, atol=1e-10)
