"""Smoke test for the out-of-sample recommender validation harness (non-shipped research)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

oos = pytest.importorskip("research.oos")


def test_leave_one_ensemble_out_runs():
    # Tiny config: a couple of ensembles, small dims, few trials.
    from precise import estimator_names

    results = oos.leave_one_ensemble_out(p=6, n_train=40, n_test=80, trials=4, seed=0)
    assert set(results) == set(oos.ENSEMBLES)
    known = set(estimator_names())
    for r in results.values():
        assert r["best_fixed"] in known
        assert r["rank_recommender"] >= 1.0  # rank 1 == the per-trial oracle
        assert r["rank_best_fixed"] >= 1.0
    assert "MEAN rank" in oos.report(results)


def test_leave_one_family_out_trained_runs():
    # Leak-free: a fresh tree is trained on the other families per held-out family. Needs sklearn.
    pytest.importorskip("sklearn")
    from precise import estimator_names

    results = oos.leave_one_family_out_trained(
        p=6, n_train=40, n_test=80, trials=3, n_problems=40, seed=0
    )
    assert set(results) == set(oos.ENSEMBLES)
    known = set(estimator_names())
    for r in results.values():
        assert r["best_fixed"] in known
        assert r["rank_recommender"] >= 1.0
        assert r["rank_best_fixed"] >= 1.0
    assert "MEAN rank" in oos.report(results)
