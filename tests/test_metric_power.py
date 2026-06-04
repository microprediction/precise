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


def test_kdim_projection_power_increases_with_k():
    # Scoring jointly in more dimensions recovers cross-direction info: k=p (full likelihood)
    # should have at least as much power as marginal (k=1) random projections.
    power, gap = metric_power.projection_power(
        p=8, k_list=(1, None), total_dirs=24, n_test=40, trials=200, seed=3
    )
    assert power[None] >= power[1]
    assert "power" in metric_power.projection_report(power, gap, p=8)


def test_full_likelihood_fails_under_high_dim_noisy_tail():
    # The headline result: with an unidentifiable noisy tail, the full likelihood is swamped
    # (~chance) while a moderate-k projection score keeps power on the recoverable bulk.
    power = metric_power.proof_high_dim(
        p=60, bulk=10, k_list=(5, None), n_test=40, trials=120, seed=0
    )
    assert power["loglik"] < 0.6  # full likelihood derailed by the tail
    assert power["proj_k5"] > power["loglik"]  # moderate-k projection does better
    assert power["proj_k60"] == pytest.approx(power["loglik"], abs=0.2)  # k=p behaves like loglik


def test_schur_gamma_recovers_power_where_full_likelihood_fails():
    # The portfolio-theory knob: shrinking the noisy cross-block coupling (gamma<1) recovers power
    # that the full likelihood (gamma=1) loses in the high-dim noisy-cross-block regime.
    power = metric_power.schur_power(
        p=60, g=6, gammas=(0.5, 1.0), n_test=60, trials=120, seed=0
    )
    assert power["gamma_0.5"] > power["full"]
    assert power["gamma_1.0"] == pytest.approx(power["full"], abs=0.2)  # gamma=1 == full likelihood
