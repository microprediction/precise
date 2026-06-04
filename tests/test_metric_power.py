"""Smoke test for the (non-shipped) metric-power experiment."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

metric_power = pytest.importorskip("research.metric_power")


def test_power_experiment_runs():
    power, gap, grid = metric_power.run(
        p=6, eps_good=0.05, eps_bad=0.12, n_grid=(20, 60), trials=40, n_dirs=20, seed=0
    )
    assert set(power) == set(metric_power.METRICS)
    assert gap > 0
    for per_n in power.values():
        for value in per_n.values():
            assert 0.0 <= value <= 1.0
    # A clear quality gap should be detected well above chance by the proper score.
    assert np.mean(list(power["loglik"].values())) > 0.6
    assert "loglik" in metric_power.report(power, gap, grid)
