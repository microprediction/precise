"""A decay rate outside (0, 1] must be rejected, not turned into an indefinite covariance.

The EWA recursion gives the newest observation weight ``r`` and the old estimate ``1 - r``. Outside
``(0, 1]`` one of those weights is negative, and the estimators returned finite, symmetric,
invertible matrices with negative eigenvalues: ``EwaCovariance(r=2.0)`` reported a minimum
eigenvalue near -100 on unit-variance data, and a minimum-variance portfolio built on it had
negative variance. ``r=0`` failed later with a bare ``ZeroDivisionError``. (#109)
"""

import inspect

import numpy as np
import pytest

from precise import AdaptiveEwaCovariance, DCCCovariance, EwaCovariance, all_estimators

RATED = [E for E in all_estimators() if "r" in inspect.signature(E).parameters]
BAD_RATES = [0.0, -0.1, 1.0 + 1e-9, 1.1, 2.0, float("nan"), float("inf"), True, "0.05", None]


def _data(n=100, p=5, seed=2026):
    return np.random.default_rng(seed).normal(size=(n, p))


def test_an_out_of_range_rate_used_to_return_an_indefinite_covariance():
    # The original failure: r=2 is accepted and the "covariance" has a large negative eigenvalue.
    with pytest.raises(ValueError, match="r must be"):
        EwaCovariance(r=2.0).fit(_data())


@pytest.mark.parametrize("Est", RATED, ids=lambda e: e.__name__)
@pytest.mark.parametrize("rate", BAD_RATES, ids=repr)
def test_bad_rate_is_rejected_on_construction(Est, rate):
    with pytest.raises(ValueError, match="r must be"):
        Est(r=rate)


@pytest.mark.parametrize("Est", RATED, ids=lambda e: e.__name__)
def test_set_params_rejects_a_bad_rate_and_leaves_the_estimator_unchanged(Est):
    X = _data()
    est = Est().fit(X)
    before = est.covariance_.copy()
    with pytest.raises(ValueError):
        est.set_params(r=1.5)
    assert est.r == 0.05
    assert np.array_equal(est.covariance_, before)
    est.partial_fit(X[:3])  # still usable
    assert est.n_samples_ == X.shape[0] + 3


@pytest.mark.parametrize("Est", RATED, ids=lambda e: e.__name__)
def test_a_rate_assigned_directly_is_caught_before_the_state_moves(Est):
    X = _data()
    est = Est().fit(X)
    n = est.n_samples_
    est.r = -0.1
    with pytest.raises(ValueError):
        est.partial_fit(X[0])
    assert est.n_samples_ == n


@pytest.mark.parametrize("Est", RATED, ids=lambda e: e.__name__)
def test_the_boundary_rate_one_is_valid_and_psd(Est):
    kwargs = {"max_r": 1.0} if Est is AdaptiveEwaCovariance else {}
    C = Est(r=1.0, **kwargs).fit(_data()).covariance_
    assert np.min(np.linalg.eigvalsh(C)) >= -1e-8


@pytest.mark.parametrize("vol_r", [0.0, -0.1, 1.5, float("nan")])
def test_dcc_volatility_rate_is_validated(vol_r):
    with pytest.raises(ValueError, match="vol_r must be"):
        DCCCovariance(vol_r=vol_r)
    DCCCovariance(vol_r=None)  # None means "same as r"


@pytest.mark.parametrize("max_r", [0.0, 1.5, float("nan")])
def test_adaptive_maximum_rate_is_validated(max_r):
    with pytest.raises(ValueError, match="max_r must be"):
        AdaptiveEwaCovariance(max_r=max_r)


def test_adaptive_maximum_rate_cannot_undercut_the_baseline():
    # With max_r < r the effective rate is always max_r, so the documented baseline never applies.
    with pytest.raises(ValueError, match="at least the baseline"):
        AdaptiveEwaCovariance(r=0.2, max_r=0.1)
