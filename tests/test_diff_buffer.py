"""diff=True must keep a snapshot of the previous level, not a view of the caller's array.

``as_rows`` does not copy a float64 array, and ``partial_fit`` stored the row itself as the previous
level. A caller that reused one buffer for each new level overwrote the stored level too, so every
difference came out as zero. (#107)
"""

import numpy as np
import pytest

from precise import EmpiricalCovariance, all_estimators

LEVELS = [100.0, 101.0, 103.0, 106.0]  # differences 1, 2, 3


def test_a_reused_buffer_gives_the_same_differences_as_fresh_arrays():
    buf = np.array([LEVELS[0]])
    est = EmpiricalCovariance(diff=True)
    est.partial_fit(buf)
    for value in LEVELS[1:]:
        buf[0] = value
        est.partial_fit(buf)
    assert np.allclose(est.location_, [2.0])
    assert np.allclose(est.covariance_, [[2.0 / 3.0]])


def test_mutating_a_consumed_batch_does_not_change_the_boundary_difference():
    X = np.array([[100.0], [101.0], [103.0]])
    est = EmpiricalCovariance(diff=True).partial_fit(X)
    X[-1, 0] = 1000.0
    est.partial_fit([106.0])
    assert np.allclose(est.location_, [2.0])


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_no_estimator_keeps_a_view_of_the_input(Est):
    if "diff" not in Est().get_params():
        pytest.skip("no diff parameter")
    X = np.random.default_rng(0).normal(size=(30, 3)).cumsum(axis=0)
    fresh = Est(diff=True)
    reused = Est(diff=True)
    buf = np.empty(3)
    for row in X:
        fresh.partial_fit(row.copy())
        buf[:] = row
        reused.partial_fit(buf)
    assert np.allclose(fresh.covariance_, reused.covariance_)
