"""Conformance tests for the covariance-estimate assessor registry."""

import numpy as np
import pytest

from precise._linalg import make_pos_def
from precise.assessment import (
    FrobeniusToTruth,
    LogLikelihood,
    all_assessors,
    assessor_from_name,
)


def _setup(p=5, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    a = rng.standard_normal((p, p))
    true_cov = a @ a.T + p * np.eye(p)
    good = true_cov.copy()  # oracle
    noise = rng.standard_normal((p, p))
    bad = make_pos_def(true_cov + 1.5 * np.linalg.norm(true_cov) * (noise + noise.T) / 2)
    X = rng.multivariate_normal(np.zeros(p), true_cov, size=n)
    return good, bad, true_cov, X


@pytest.mark.parametrize("assessor", all_assessors(), ids=lambda a: a.name)
def test_prefers_the_better_estimate(assessor):
    good, bad, true_cov, X = _setup()
    kw = {"X_test": X, "true_cov": true_cov}
    s_good = assessor.score(good, **kw)
    s_bad = assessor.score(bad, **kw)
    assert np.isfinite(s_good) and np.isfinite(s_bad)
    assert s_good > s_bad, f"{assessor.name}: oracle {s_good:.3f} should beat bad {s_bad:.3f}"


def test_capability_flags():
    assert LogLikelihood().usable(have_data=True, have_truth=False)
    assert not LogLikelihood().usable(have_data=False, have_truth=False)
    # truth-based assessor needs the true covariance
    assert FrobeniusToTruth().usable(have_data=False, have_truth=True)
    assert not FrobeniusToTruth().usable(have_data=True, have_truth=False)


def test_registry():
    assessors = all_assessors()
    assert len(assessors) >= 6
    assert assessor_from_name("BlockPseudoLikelihood").name == "BlockPseudoLikelihood"
    with pytest.raises(KeyError):
        assessor_from_name("NoSuchAssessor")
