"""A row of the wrong width must be rejected, not broadcast across the fixed-dimensional state.

``partial_fit`` never compared later rows with ``n_features_in_``. A one-element row was broadcast
to every column: after ``[0.01, -0.02]`` and a malformed ``[0.5]``, ``EmpiricalCovariance`` reported
the statistics of ``[0.5, 0.5]`` with no warning. A wider row expanded the estimate while
``n_features_in_`` still said one. ``score`` of a short row also subtracted the wrong Gaussian
normalization. (#103)
"""

import numpy as np
import pytest

from precise import (
    ConditionalCovariance,
    EmpiricalCovariance,
    EwaCovariance,
    all_estimators,
)

ESTIMATORS = all_estimators()


def _data(n=60, p=3, seed=0):
    return np.random.default_rng(seed).normal(size=(n, p))


def test_a_short_row_used_to_be_broadcast_into_the_estimate():
    est = EmpiricalCovariance()
    est.partial_fit([0.01, -0.02])
    with pytest.raises(ValueError, match="has 2 features but got rows with 1"):
        est.partial_fit([0.50])
    assert est.n_samples_ == 1
    assert np.allclose(est.location_, [0.01, -0.02])


def test_a_wide_row_used_to_expand_the_estimate_past_n_features_in():
    est = EmpiricalCovariance()
    est.partial_fit([0.0])
    with pytest.raises(ValueError):
        est.partial_fit([1.0, 2.0])
    assert est.n_features_in_ == 1
    assert est.covariance_.shape == (1, 1)


@pytest.mark.parametrize("Est", ESTIMATORS, ids=lambda e: e.__name__)
@pytest.mark.parametrize("bad_width", [1, 4])
def test_wrong_width_is_rejected_and_leaves_the_estimator_untouched(Est, bad_width):
    X = _data()
    est = Est().fit(X)
    n, cov, loc = est.n_samples_, est.covariance_.copy(), est.location_.copy()
    bad = np.full(bad_width, 0.5)
    with pytest.raises(ValueError, match="fixed dimension"):
        est.partial_fit(bad)
    with pytest.raises(ValueError, match="fixed dimension"):
        est.partial_fit(np.full((2, bad_width), 0.5))  # a batch too
    assert est.n_samples_ == n
    assert np.array_equal(est.covariance_, cov)
    assert np.array_equal(est.location_, loc)
    est.partial_fit(X[0])  # a correct row still goes through
    assert est.n_samples_ == n + 1


@pytest.mark.parametrize("Est", ESTIMATORS, ids=lambda e: e.__name__)
def test_scoring_rejects_wrong_width(Est):
    est = Est().fit(_data())
    with pytest.raises(ValueError, match="fixed dimension"):
        est.mahalanobis([0.5])
    with pytest.raises(ValueError, match="fixed dimension"):
        est.score([0.5])


def test_diff_checks_the_raw_level_before_differencing():
    est = EmpiricalCovariance(diff=True)
    est.partial_fit([100.0, 200.0])  # first level, stored only
    with pytest.raises(ValueError, match="has 2 features"):
        est.partial_fit([101.0])
    assert np.array_equal(est._prev_x, [100.0, 200.0])


def test_continuing_from_a_restored_state_checks_its_dimension():
    est = EwaCovariance().fit(_data(p=3))
    restored = EwaCovariance().set_state(est.get_state())
    with pytest.raises(ValueError, match="has 3 features"):
        restored.partial_fit([0.1, 0.2])


def test_conditional_covariance_rejects_before_updating_any_sub_model():
    est = ConditionalCovariance().fit(_data(n=40, p=2))
    corr_n = est._corr_model.n_samples_
    vol_n = [vm._est.n_samples_ for vm in est._vol_models]
    with pytest.raises(ValueError, match="fixed dimension"):
        est.partial_fit([0.5])
    assert est._corr_model.n_samples_ == corr_n
    assert [vm._est.n_samples_ for vm in est._vol_models] == vol_n
