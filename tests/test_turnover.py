"""Smoke test for the (non-shipped) turnover study, plus the finding it exists to record."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

turnover = pytest.importorskip("research.turnover")


def test_matched_decay_inverts_the_effective_sample_size():
    for w in (60, 125, 250, 500):
        r = turnover.matched_decay(w)
        assert np.isclose((2 - r) / r, w)


def test_impulse_baseline_survives_an_early_shock():
    # A shock early in the stream must not produce an empty baseline slice (and a nan ratio).
    res = turnover.impulse_response(p=8, window=40, n=300, shock_at=120, seeds=2)
    for v in res.values():
        assert np.isfinite(v["arrival"]) and np.isfinite(v["echo"]) and v["baseline"] > 0


def test_mv_weights_sum_to_one_and_survive_a_singular_input():
    rng = np.random.default_rng(0)
    A = rng.standard_normal((6, 6))
    assert np.isclose(turnover.mv_weights(A @ A.T + np.eye(6)).sum(), 1.0)
    assert np.isclose(turnover.mv_weights(np.zeros((6, 6))).sum(), 1.0)


def test_window_echoes_at_the_boundary_and_exponential_decay_does_not():
    # The finding this module exists for: a shock is paid for twice by a hard window -- once on
    # arrival, once W periods later when it drops out and the estimate jumps back for no reason.
    res = turnover.impulse_response(p=16, window=125, n=900, shock_at=450, seeds=6)
    win = next(v for k, v in res.items() if k.startswith("window"))
    ewa = next(v for k, v in res.items() if k.startswith("EW"))
    assert win["arrival"] > 3.0 and ewa["arrival"] > 3.0, "both must react to the shock itself"
    assert win["echo"] > 3.0, "the window must show a boundary echo"
    assert win["echo"] > 1.8 * ewa["echo"], "exponential decay must not echo the way a window does"


def test_portfolio_reports_risk_and_turnover_for_every_arm():
    res = turnover.portfolio(p=8, n=400, seeds=1, burn=100, window=60)
    assert "NLS window W=60" in res and "EW-NLS n_eff" in res
    for v in res.values():
        assert v["ann_vol"] > 0 and v["turnover"] >= 0 and v["ann_cost"] >= 0
