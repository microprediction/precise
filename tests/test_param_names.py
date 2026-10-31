"""Reject misspelled/non-parameter keys before mutating an estimator (#106)."""

import pickle

import numpy as np
import pytest

from precise import EwaCovariance, all_estimators


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_unknown_parameter_rejected_for_every_estimator(Est):
    est = Est()
    before = pickle.dumps(est)
    with pytest.raises(ValueError, match="Invalid parameter.*rr.*Valid parameters"):
        est.set_params(rr=0.9)
    assert pickle.dumps(est) == before
    assert not hasattr(est, "rr")


@pytest.mark.parametrize("fitted", [False, True])
@pytest.mark.parametrize("unknown_first", [False, True])
def test_mixed_known_and_unknown_keys_are_atomic(fitted, unknown_first):
    est = EwaCovariance(r=0.05, diff=True)
    if fitted:
        est.fit(np.arange(20).reshape(10, 2))
    before = pickle.dumps(est)
    params = {"rr": 0.9, "r": 0.2} if unknown_first else {"r": 0.2, "rr": 0.9}
    with pytest.raises(ValueError, match="Invalid parameter"):
        est.set_params(**params)
    assert pickle.dumps(est) == before
    assert not hasattr(est, "rr")


@pytest.mark.parametrize("key", ["_state", "n_features_in_", "_validate_params"])
def test_existing_non_parameter_attributes_are_not_assignable(key):
    est = EwaCovariance().fit([[1, 2], [3, 4]])
    before = pickle.dumps(est)
    with pytest.raises(ValueError, match="Invalid parameter"):
        est.set_params(**{key: None})
    assert pickle.dumps(est) == before


def test_valid_unfitted_params_and_empty_request_keep_existing_contract():
    est = EwaCovariance()
    assert est.set_params(r=0.2, diff=True) is est
    assert est.get_params() == {"r": 0.2, "diff": True}
    assert est.set_params() is est
    est.fit([[1, 2], [3, 5]])
    assert est._state["r"] == 0.2
    before = pickle.dumps(est)
    assert est.set_params() is est
    assert pickle.dumps(est) == before
