"""Guard the verified half of the spiked-model analysis: the gamma=1 variance blow-up (research)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

sp = pytest.importorskip("research.schur_spiked")


def test_gamma1_variance_blows_up_with_conditioning():
    p, sizes, n = 12, [4, 4, 4], 60

    def var_at(bulk, gamma):
        Sig_t, _, _ = sp._spiked(p, spike=12.0, bulk=bulk, seed=1)
        G = sp._grad_score_gap(Sig_t, sizes, gamma, Sig_t, 0.5, 0.05)
        return sp._cov_quadform(G, Sig_t, n)

    # As lambda_min shrinks (bulk: 0.4 -> 0.05) the gamma=1 score-gap variance grows sharply...
    v_full = [var_at(b, 1.0) for b in (0.4, 0.15, 0.05)]
    assert v_full[0] < v_full[1] < v_full[2]
    assert v_full[2] > 5 * v_full[0]
    # ...while gamma=0.3 stays comparatively bounded (smaller blow-up at the worst conditioning).
    v_damp = [var_at(b, 0.3) for b in (0.4, 0.15, 0.05)]
    assert v_damp[2] < v_full[2]


def test_delta_variance_is_closed_form_quadform():
    # _cov_quadform(G, Sig, n) == (2/n) tr((G Sig)^2), the Gaussian sampling-cov contraction.
    import numpy as np

    rng = np.random.default_rng(0)
    A = rng.standard_normal((5, 5))
    G = A + A.T
    Sig = sp._spiked(5, seed=3)[0]
    M = G @ Sig
    assert sp._cov_quadform(G, Sig, 40) == pytest.approx((2.0 / 40) * np.trace(M @ M), rel=1e-9)
