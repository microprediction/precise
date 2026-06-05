"""Guard the closed-form gamma* in the tractable two-block case (research)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

gs = pytest.importorskip("research.schur_gamma_star")


def test_closed_form_matches_simulated_argmin():
    # gamma* = (n-2) rho^2 / ((n-2) rho^2 + (1-rho^2)) matches the simulated argmin of R(gamma).
    for n in (5, 10, 30):
        for rho2 in (0.1, 0.3, 0.6, 0.9):
            gc = gs.gamma_star(n, rho2)
            ge = gs.empirical_gamma_star(rho2, n, n_draws=12000, seed=n * 100 + int(100 * rho2))
            assert abs(gc - ge) < 0.05  # within grid (0.02) + Monte-Carlo resolution


def test_limits_and_monotonicity():
    # rho^2 -> 0 gives gamma* -> 0; rho^2 -> 1 gives gamma* -> 1; n -> inf gives gamma* -> 1.
    assert gs.gamma_star(30, 1e-6) < 1e-3
    assert gs.gamma_star(30, 1 - 1e-6) > 0.999
    assert gs.gamma_star(10_000, 0.3) > 0.99
    # increasing in n (fixed rho^2) and in rho^2 (fixed n)
    g_n = [gs.gamma_star(n, 0.4) for n in (3, 5, 10, 30, 100)]
    assert all(b > a for a, b in zip(g_n, g_n[1:]))
    g_r = [gs.gamma_star(20, r) for r in (0.05, 0.2, 0.5, 0.8, 0.99)]
    assert all(b > a for a, b in zip(g_r, g_r[1:]))


def test_n_equals_three_is_rho2():
    # at n=3, gamma* = rho^2 exactly ((n-2)=1).
    for rho2 in (0.2, 0.5, 0.8):
        assert gs.gamma_star(3, rho2) == pytest.approx(rho2)
