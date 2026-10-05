"""A diff=True stream resumed from get_state/set_state must equal the uninterrupted stream.

The checkpoint held only the estimator state, not the last raw level, so a restored estimator used
the first level after the boundary to start a new difference and silently dropped the one that
crossed it: on levels 0, 1, 3 | 103, 107, 112 the boundary jump of 100 vanished, giving mean 3 and
variance 2.5 instead of 22.4 and 1507.44. ``set_state(None)`` also kept the previous stream's
level. (#86)
"""

import json
import pickle

import numpy as np
import pytest

from precise import EmpiricalCovariance, all_estimators

DIFF_ESTIMATORS = [E for E in all_estimators() if "diff" in E().get_params()]


def test_the_boundary_difference_survives_a_json_checkpoint():
    X = np.array([[0.0], [1.0], [3.0], [103.0], [107.0], [112.0]])  # differences 1, 2, 100, 4, 5
    before = EmpiricalCovariance(diff=True).fit(X[:3])
    state = json.loads(json.dumps(before.get_state()))
    resumed = EmpiricalCovariance(diff=True).set_state(state)
    resumed.partial_fit(X[3:])
    assert resumed.n_samples_ == 5
    assert np.allclose(resumed.location_, [22.4])
    assert np.allclose(resumed.covariance_, [[1507.44]])


@pytest.mark.parametrize("Est", DIFF_ESTIMATORS, ids=lambda e: e.__name__)
@pytest.mark.parametrize("split", [1, 40])
def test_resumed_stream_equals_uninterrupted_stream(Est, split):
    rng = np.random.default_rng(5)
    X = 100.0 + rng.normal(size=(80, 3)).cumsum(axis=0)
    X[split:] += 25.0  # a large move across the checkpoint
    full = Est(diff=True).fit(X)
    before = Est(diff=True).fit(X[:split])
    resumed = Est(diff=True).set_state(json.loads(json.dumps(before.get_state())))
    resumed.partial_fit(X[split:])
    assert resumed.n_samples_ == full.n_samples_
    assert np.allclose(resumed.location_, full.location_)
    assert np.allclose(resumed.covariance_, full.covariance_)


def test_clearing_the_state_forgets_the_previous_level():
    e = EmpiricalCovariance(diff=True).fit([[0.0], [10.0]])
    e.set_state(None)
    e.partial_fit([20.0])
    assert e.n_samples_ == 0


def test_restoring_replaces_a_stale_previous_level():
    e = EmpiricalCovariance(diff=True).fit([[0.0], [1000.0]])
    other = EmpiricalCovariance(diff=True).fit([[0.0], [1.0], [3.0]])
    e.set_state(other.get_state())
    e.partial_fit([6.0])
    assert np.allclose(e.location_, [2.0])  # differences 1, 2, 3


def test_a_checkpoint_without_prev_x_warns():
    state = EmpiricalCovariance(diff=True).fit([[0.0], [1.0], [3.0]]).get_state()
    del state["prev_x"]
    with pytest.warns(UserWarning, match="no prev_x"):
        EmpiricalCovariance(diff=True).set_state(state)


def test_pickle_still_resumes_exactly():
    X = np.array([[0.0], [1.0], [3.0], [103.0], [107.0]])
    e = pickle.loads(pickle.dumps(EmpiricalCovariance(diff=True).fit(X[:3])))
    e.partial_fit(X[3:])
    assert np.allclose(e.location_, EmpiricalCovariance(diff=True).fit(X).location_)
