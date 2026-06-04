"""Conformance contract for the positional online covariance estimators.

A single parametrized test over ``all_estimators()`` replaces hundreds of ad-hoc tests:
feed every registered estimator the same stream and assert the shared invariants.
"""

import numpy as np
import pytest

from precise import EmpiricalCovariance, all_estimators, estimator_from_name


def _random_spd(n, rng):
    a = rng.standard_normal((n, n))
    return a @ a.T + n * np.eye(n)


def _sample(n_dim=4, n_obs=600, seed=0):
    rng = np.random.default_rng(seed)
    cov = _random_spd(n_dim, rng)
    mean = rng.standard_normal(n_dim)
    X = rng.multivariate_normal(mean, cov, size=n_obs)
    return X, cov, mean


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_contract(Est):
    X, _, _ = _sample()
    est = Est()

    # Streaming one observation at a time.
    for row in X:
        est.partial_fit(row)

    n = X.shape[1]
    C = est.covariance_
    assert C.shape == (n, n)
    assert np.allclose(C, C.T, atol=1e-8), "covariance_ must be symmetric"
    assert np.min(np.linalg.eigvalsh(C)) >= -1e-8, "covariance_ must be PSD"

    corr = est.correlation_
    assert np.allclose(np.diag(corr), 1.0, atol=1e-6), "correlation_ unit diagonal"

    prec = est.precision_
    assert np.allclose(prec @ C, np.eye(n), atol=1e-4), "precision_ @ covariance_ == I"

    assert est.location_.shape == (n,)
    assert est.n_samples_ == X.shape[0]
    assert np.isfinite(est.score(X))
    assert est.mahalanobis(X).shape == (X.shape[0],)


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_fit_equals_stream(Est):
    X, _, _ = _sample()
    streamed = Est()
    for row in X:
        streamed.partial_fit(row)
    batched = Est().fit(X)
    assert np.allclose(streamed.covariance_, batched.covariance_, atol=1e-10)
    assert np.allclose(streamed.location_, batched.location_, atol=1e-10)


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_state_roundtrip(Est):
    X, _, _ = _sample()
    est = Est().fit(X)
    state = est.get_state()
    restored = Est().set_state(state)
    assert np.allclose(restored.covariance_, est.covariance_, atol=1e-12)
    assert np.allclose(restored.location_, est.location_, atol=1e-12)


def test_registry_lookup():
    assert estimator_from_name("EmpiricalCovariance") is EmpiricalCovariance
    with pytest.raises(KeyError):
        estimator_from_name("NoSuchEstimator")


def test_empirical_matches_numpy():
    # Population covariance (bias=True) is the empirical/MLE convention sklearn also uses.
    X, _, _ = _sample(n_dim=5, n_obs=2000, seed=3)
    est = EmpiricalCovariance().fit(X)
    assert np.allclose(est.covariance_, np.cov(X, rowvar=False, bias=True), atol=1e-8)
    assert np.allclose(est.location_, X.mean(axis=0), atol=1e-8)
    assert np.allclose(est.correlation_, np.corrcoef(X, rowvar=False), atol=1e-6)


def test_diff_estimates_differences():
    X, _, _ = _sample(n_dim=3, n_obs=400, seed=2)
    est = EmpiricalCovariance(diff=True).fit(X)
    expected = np.cov(np.diff(X, axis=0), rowvar=False, bias=True)
    assert np.allclose(est.covariance_, expected, atol=1e-8)
    assert est.n_samples_ == X.shape[0] - 1
