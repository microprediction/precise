"""Smoke test for the (non-shipped) expanding-vs-window study, so it does not rot."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

forgetting = pytest.importorskip("research.forgetting")


def test_run_scores_every_arm_on_every_scenario():
    results = forgetting.run(p=8, n=400, seeds=1, burn=100, every=50)
    assert set(results) == set(forgetting.scenarios(8, 400, np.random.default_rng(0)))
    for cells in results.values():
        assert "NLS (exp)" in cells and "raw window W=60" in cells
        assert all(np.isfinite(v) and v >= 0 for v in cells.values())
    assert "scenario" in forgetting.report(results)


def test_shrinkage_helps_at_every_window_length():
    # The claim that makes a short window affordable: cleaning the window's spectrum must beat
    # leaving it raw, at every window length, in every regime.
    results = forgetting.run(p=16, n=1200, seeds=1, burn=300, every=50)
    for scenario, cells in results.items():
        for w in forgetting.WINDOWS:
            assert cells[f"NLS W={w}"] < cells[f"raw window W={w}"], (scenario, w)
