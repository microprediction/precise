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


def _rng(seed):
    import numpy as np

    return np.random.default_rng(seed)


def test_general_recovers_predictive_law_and_closed_form_is_maximizer():
    # Vector two-block: every block's conditional law is recovered, and the closed form is the
    # maximizer of the exact expected gamma-Schur log-lik (local search finds nothing better).
    import numpy as np

    Sig_true = thy._random_spd(5, _rng(1))
    for gamma in (1.0, 0.9, 0.7):
        Sig = thy.closed_form_general(Sig_true, [3, 2], gamma)
        assert thy._is_spd(Sig)
        # effective regression == true regression; damped conditional cov == true Schur complement
        tWW, tKW = Sig_true[:3, :3], Sig_true[3:, :3]
        Bstar = tKW @ np.linalg.inv(tWW)
        Sstar = Sig_true[3:, 3:] - Bstar @ tKW.T
        cWW, cKW = Sig[:3, :3], Sig[3:, :3]
        Geff = gamma * cKW @ np.linalg.inv(cWW)
        Sg = Sig[3:, 3:] - gamma * cKW @ np.linalg.solve(cWW, cKW.T)
        assert np.allclose(Geff, Bstar, atol=1e-6)
        assert np.allclose(Sg, Sstar, atol=1e-6)
        gap = thy._local_search_confirms(Sig_true, [3, 2], gamma, iters=2000)
        assert gap <= 1e-6  # closed form is the (local) maximizer


def test_general_psd_threshold_is_top_canonical_correlation():
    # Two vector blocks: PSD boundary is governed by the LARGEST squared canonical correlation.
    Sig_true = thy._random_spd(5, _rng(1))
    rho2_max = thy.canonical_corr2(Sig_true, 3)[0]
    gmin = thy._solve_spd_threshold(rho2_max)
    assert thy._is_spd(thy.closed_form_general(Sig_true, [3, 2], gmin + 0.03))
    assert not thy._is_spd(thy.closed_form_general(Sig_true, [3, 2], gmin - 0.03))
