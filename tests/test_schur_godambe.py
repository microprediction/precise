"""Regression guard for the discrimination/Godambe results (research)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

gd = pytest.importorskip("research.schur_godambe")
thy = pytest.importorskip("research.schur_likelihood_theory")


def test_W1_is_the_inverse():
    # gamma=1 Schur operator reconstructs the precision exactly (block LDL^T).
    import numpy as np

    Sig, _, _ = gd._spiked(6, seed=2)
    W1, _ = gd.schur_operator(Sig, [2, 2, 2], 1.0)
    assert np.allclose(W1, np.linalg.inv(Sig), atol=1e-9)


def test_closed_form_snr_matches_monte_carlo():
    St, A, B = gd._noise_subspace_pair(6, eps_a=0.05, eps_b=0.15, seed=3)
    for g in (1.0, 0.6, 0.3):
        exact = gd.snr(A, B, St, [3, 3], g)
        mc = gd.snr_montecarlo(A, B, St, [3, 3], g, n=200000, seed=1)
        assert abs(exact - mc) < 0.02


def test_score_unbiased_only_at_endpoints():
    # grad of expected ell_gamma at the truth: ~0 at gamma in {0,1}, nonzero in the interior.
    import numpy as np

    St, _, _ = gd._spiked(6, seed=2)
    sizes, p, h = [3, 3], 6, 1e-5

    def grad_norm(g):
        tot = 0.0
        for i in range(p):
            for j in range(i, p):
                E = np.zeros((p, p))
                E[i, j] = E[j, i] = 1.0
                d = (thy.expected_schur_loglik(St, St + h * E, sizes, g)
                     - thy.expected_schur_loglik(St, St - h * E, sizes, g)) / (2 * h)
                tot += d * d
        return np.sqrt(tot)

    assert grad_norm(1.0) < 1e-3   # full likelihood: unbiased
    assert grad_norm(0.0) < 1e-3   # block-marginal: unbiased (identified params)
    assert grad_norm(0.5) > 1e-1   # interior: biased (tempered/misspecified score)


def test_interior_gamma_optimum_in_structured_regime():
    # The principled W_gamma operator exhibits an interior-gamma power peak that beats both
    # endpoints, when signal is within-block and noise is shared between-block.
    sp = gd.structured_power_over_draws(p=60, g=6, trials=120, n_test=70, seed=0)
    best = max(sp, key=sp.get)
    assert 0.0 < best < 1.0                       # the optimum is interior
    assert sp[best] > sp[1.0] + 0.05              # beats the full likelihood
    assert sp[best] > sp[0.0] + 0.05              # beats the block-diagonal endpoint
