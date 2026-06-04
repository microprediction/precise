"""Smoke test for the (non-shipped) research bake-off, so it does not rot."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

bakeoff = pytest.importorskip("research.bakeoff")

from precise import estimator_names  # noqa: E402


def test_bakeoff_runs_and_ranks_every_estimator():
    results = bakeoff.run(d=4, n=300, n_test=100, seed=0)
    assert set(results) == set(estimator_names())
    # Every estimator was scored on every scenario.
    scenarios = next(iter(results.values()))
    assert len(scenarios) >= 5
    # Every estimate is scored by the assessor registry (assessor-name -> score).
    from precise.assessment import all_assessors

    assessor_names = {a.name for a in all_assessors()}
    for cells in results.values():
        for scores in cells.values():
            assert set(scores) <= assessor_names and len(scores) >= 3

    board = bakeoff.leaderboard(results)
    assert "avg_rank" in board
    assert "EmpiricalCovariance" in board
    assert "Winner" in bakeoff.per_scenario_winners(results)
