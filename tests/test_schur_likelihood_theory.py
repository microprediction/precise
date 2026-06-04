"""Regression guard for the worked two-block model in the Schur-likelihood paper (research)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

thy = pytest.importorskip("research.schur_likelihood_theory")


def test_effective_law_recovered_for_every_gamma():
    # The population gamma-Schur maximizer recovers the TRUE predictive law (beta=b*, S(gamma)=s*)
    # for every gamma, while the implied covariance inflates (C_hat = Sig12*/gamma).
    a, b_star, s_star = 1.0, 0.8, 0.5
    for gamma in (1.0, 0.9, 0.7, 0.5, 0.3, 0.1):
        A, C, D = thy.closed_form_maximizer(a, b_star, s_star, gamma)
        beta = gamma * C / A
        s_gamma = D - gamma * C * C / A
        assert beta == pytest.approx(b_star, abs=1e-9)       # effective coef recovers truth
        assert s_gamma == pytest.approx(s_star, abs=1e-9)    # damped conditional var recovers truth
        assert C == pytest.approx(b_star * a / gamma, abs=1e-9)  # implied cov inflates by 1/gamma


def test_psd_exit_threshold_matches_closed_form():
    # The free maximizer is SPD exactly above gamma_min(rho^2); below it leaves the cone.
    a, b_star, s_star = 1.0, 0.8, 0.5
    e = b_star**2 * a
    rho2 = e / (e + s_star)
    gmin = thy._solve_spd_threshold(rho2)
    assert 0.0 < gmin < 1.0
    for gamma in (gmin + 0.05, gmin + 0.2):
        A, C, D = thy.closed_form_maximizer(a, b_star, s_star, gamma)
        assert A * D - C * C > 0
        assert thy.spd_threshold_holds(a, b_star, s_star, gamma)
    for gamma in (gmin - 0.05, gmin - 0.2):
        if gamma <= 0:
            continue
        A, C, D = thy.closed_form_maximizer(a, b_star, s_star, gamma)
        assert A * D - C * C <= 0
        assert not thy.spd_threshold_holds(a, b_star, s_star, gamma)


def test_threshold_increases_with_coupling():
    # Stronger block coupling rho^2 -> larger usable-gamma floor (-> 1 as rho^2 -> 1).
    gmins = [thy._solve_spd_threshold(r) for r in (0.1, 0.4, 0.7, 0.95)]
    assert all(b > a for a, b in zip(gmins, gmins[1:]))
