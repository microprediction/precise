"""A NaN or inf observation must be rejected, not absorbed into the running state for good.

One non-finite value entered the running moments of 19 of the 20 registered estimators and stayed
there: after 100 clean rows, one NaN and 100 more clean rows, twelve returned a non-finite
covariance and seven failed later inside a decomposition. (#89)
"""

import numpy as np
import pytest

from precise import ConditionalCovariance, EmpiricalCovariance, FixedUniverse, all_estimators


def _data(n=100, p=4, seed=20260925):
    return np.random.default_rng(seed).standard_normal((n, p))


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
def test_non_finite_row_is_rejected_and_the_estimate_survives(Est, bad):
    X = _data()
    est = Est().fit(X)
    n, cov = est.n_samples_, est.covariance_.copy()
    with pytest.raises(ValueError, match="must be finite"):
        est.partial_fit([0.1, bad, -0.2, 0.3])
    with pytest.raises(ValueError, match="must be finite"):  # the clean rows before it are not kept
        est.partial_fit(np.vstack([X[:2], [[0.1, bad, -0.2, 0.3]]]))
    assert est.n_samples_ == n
    assert np.array_equal(est.covariance_, cov)
    est.partial_fit(_data(seed=1))
    assert np.all(np.isfinite(est.covariance_))


def test_diff_rejects_before_storing_the_level():
    est = EmpiricalCovariance(diff=True)
    est.partial_fit([1.0, 2.0])
    with pytest.raises(ValueError):
        est.partial_fit([np.nan, 3.0])
    assert np.array_equal(est._prev_x, [1.0, 2.0])


def test_conditional_covariance_rejects_before_updating_any_sub_model():
    est = ConditionalCovariance().fit(_data(n=40, p=2))
    corr_n = est._corr_model.n_samples_
    with pytest.raises(ValueError, match="must be finite"):
        est.partial_fit([0.5, np.nan])
    assert est._corr_model.n_samples_ == corr_n


def test_fixed_universe_does_not_remember_a_rejected_value():
    u = FixedUniverse(keys=["a", "b"])
    u.update({"a": 0.1, "b": 0.2})
    with pytest.raises(ValueError):
        u.update({"a": np.nan, "b": 0.3})
    u.update({"b": 0.4})  # "a" is forward-filled from 0.1, not from the rejected NaN
    cov, _ = u.cov_array()
    assert np.all(np.isfinite(cov))
