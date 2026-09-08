"""Properties of the analytical nonlinear shrinkage estimator.

The shared contract (PSD, symmetry, fit==stream, state round-trip) is already exercised for
every registered estimator by ``tests/test_estimators.py``. What is tested here is what makes
this estimator *right* rather than merely well-formed: the shrinkage vanishes as the sample
grows, it stays finite where the sample covariance is singular, and it does not mangle a
spectrum with a dominant mode.
"""

import numpy as np
import pytest

from precise import NonlinearShrinkageCovariance
from precise.nonlinear_shrinkage import nonlinear_shrinkage_spectrum


def _market_cov(p, seed=0):
    """One dominant common mode over a modest bulk -- the equity shape."""
    rng = np.random.default_rng(seed)
    m = np.ones((p, 1)) * 0.8
    B = rng.standard_normal((p, 3)) / np.sqrt(3) * 0.3
    return m @ m.T + B @ B.T + np.diag(0.3 + 0.4 * rng.random(p))


def _bulk_cov(p, seed=0):
    """A broad spectrum with no dominant mode."""
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((p, 2 * p))
    C = A @ A.T / (2 * p)
    return C / np.trace(C) * p


def _draw(C0, n, seed=0):
    rng = np.random.default_rng(seed + 7)
    return rng.multivariate_normal(np.zeros(C0.shape[0]), C0, size=n)


def _rel_err(A, B):
    return float(np.linalg.norm(A - B) / np.linalg.norm(B))


def _nll(C, X):
    sign, logdet = np.linalg.slogdet(C)
    assert sign > 0
    quad = np.einsum("ij,jk,ik->i", X, np.linalg.inv(C), X)
    return float(0.5 * (logdet + quad.mean()))


def test_shrinkage_vanishes_as_sample_grows():
    # With p fixed the sample covariance is already consistent, so the map must back off.
    C0 = _bulk_cov(10)
    gaps = []
    for n in (200, 2000, 20000):
        X = _draw(C0, n)
        est = NonlinearShrinkageCovariance().fit(X)
        gaps.append(_rel_err(est.covariance_, np.cov(X, rowvar=False, bias=True)))
    assert gaps[0] > gaps[1] > gaps[2], f"shrinkage should decay with n, got {gaps}"
    assert gaps[-1] < 0.01


@pytest.mark.parametrize("cov_fn", [_bulk_cov, _market_cov], ids=["bulk", "market_mode"])
def test_beats_sample_covariance_out_of_sample(cov_fn):
    p, n = 60, 120  # q = 0.5: high-dimensional enough that the sample covariance is poor
    C0 = cov_fn(p)
    X, X_out = _draw(C0, n), _draw(C0, 2000, seed=99)
    shrunk = NonlinearShrinkageCovariance().fit(X).covariance_
    sample = np.cov(X, rowvar=False, bias=True)
    assert _nll(shrunk, X_out) < _nll(sample, X_out)
    assert np.linalg.cond(shrunk) < np.linalg.cond(sample)


def test_dominant_mode_is_not_flattened():
    # Regression guard. A cleaner derived for a bulk will happily shrink an isolated market
    # mode as though it were noise: that leaves the held-out likelihood looking fine while the
    # matrix itself is badly wrong. Frobenius error catches it; likelihood alone does not.
    p, n = 80, 160
    C0 = _market_cov(p)
    X = _draw(C0, n)
    shrunk = NonlinearShrinkageCovariance().fit(X).covariance_
    sample = np.cov(X, rowvar=False, bias=True)
    assert _rel_err(shrunk, C0) <= _rel_err(sample, C0) * 1.05
    # The leading eigenvalue must survive roughly intact, not be pulled into the bulk.
    assert np.linalg.eigvalsh(shrunk)[-1] > 0.8 * np.linalg.eigvalsh(sample)[-1]


def test_finite_and_invertible_when_p_exceeds_n():
    p, n = 120, 60
    C0 = _market_cov(p)
    X, X_out = _draw(C0, n), _draw(C0, 2000, seed=99)
    est = NonlinearShrinkageCovariance().fit(X)
    C = est.covariance_
    assert np.all(np.isfinite(C))
    assert np.linalg.eigvalsh(C).min() > 0, "must be strictly PD where the sample is singular"
    assert np.isfinite(_nll(C, X_out))
    assert np.allclose(est.precision_ @ C, np.eye(p), atol=1e-6)


def test_spectrum_map_is_scale_equivariant():
    lam = np.sort(np.abs(np.random.default_rng(3).standard_normal(40))) + 0.1
    base = nonlinear_shrinkage_spectrum(lam, 200)
    scaled = nonlinear_shrinkage_spectrum(lam * 7.5, 200)
    assert np.allclose(scaled, base * 7.5, rtol=1e-10)


def test_falls_back_to_sample_when_too_few_observations():
    assert nonlinear_shrinkage_spectrum(np.arange(1.0, 6.0), n=5) is None
    X = _draw(_bulk_cov(4), 6)
    est = NonlinearShrinkageCovariance().fit(X)
    assert np.allclose(est.covariance_, np.cov(X, rowvar=False, bias=True), atol=1e-10)


def test_memo_invalidates_on_update_and_restore():
    X = _draw(_bulk_cov(6), 200)
    est = NonlinearShrinkageCovariance().fit(X)
    before = est.covariance_.copy()
    est.partial_fit(_draw(_bulk_cov(6), 50, seed=5))
    assert not np.allclose(before, est.covariance_), "memo must not survive an update"

    other = NonlinearShrinkageCovariance().fit(_draw(_market_cov(6), 200, seed=11))
    stale = other.covariance_.copy()
    other.set_state(est.get_state())
    assert not np.allclose(stale, other.covariance_), "memo must not survive set_state"
    assert np.allclose(other.covariance_, est.covariance_, atol=1e-12)


def test_rank_deficient_stream_degrades_gracefully():
    # Collinear inputs make the sample covariance singular however many observations arrive.
    # Three of the seven directions carry no variance at all: the estimator must neither blow up
    # nor invent variance for them -- a singular truth deserves a singular estimate.
    rng = np.random.default_rng(4)
    Z = rng.standard_normal((400, 4))
    X = np.column_stack([Z, Z @ rng.standard_normal((4, 3))])  # 7 columns spanning rank 4
    sample = np.cov(X, rowvar=False, bias=True)
    assert np.linalg.matrix_rank(sample) == 4

    C = NonlinearShrinkageCovariance().fit(X).covariance_
    assert np.all(np.isfinite(C))
    assert np.linalg.eigvalsh(C).min() > -1e-10, "PSD up to numerical noise"
    lam = np.sort(np.linalg.eigvalsh(C))
    assert np.all(lam[:3] < 1e-8), "null directions must not be handed invented variance"
    assert lam[3] > 0.1, "the four real directions must survive"
    # And the informative part is genuinely cleaned, not passed through untouched.
    assert not np.allclose(C, sample, atol=1e-8)


# --------------------------------------------------------------- the rolling-window counterpart


def test_window_matches_an_explicit_recomputation():
    # The rolling sums are maintained by add-and-drop; they must agree with the covariance of the
    # last `window` rows computed from scratch.
    from precise import WindowedNonlinearShrinkageCovariance

    W = 40
    X = _draw(_bulk_cov(5), 300)
    est = WindowedNonlinearShrinkageCovariance(window=W).fit(X)
    cov, n = est._spectrum_inputs(est._state)
    assert n == W - 1
    assert np.allclose(cov, np.cov(X[-W:], rowvar=False, bias=True), atol=1e-10)
    assert np.allclose(est.location_, X[-W:].mean(axis=0), atol=1e-10)
    assert est.n_samples_ == 300, "n_samples_ counts the stream, not the window"


def test_add_and_drop_does_not_drift_over_a_long_stream():
    # Cancellation accumulates in a running add-and-drop. Over many windows the maintained sums
    # must still match a from-scratch recomputation, which is what the periodic refresh buys.
    from precise import WindowedNonlinearShrinkageCovariance

    W = 25
    rng = np.random.default_rng(8)
    # A large offset is the hostile case for cancellation in a running add-and-drop.
    X = rng.standard_normal((4000, 4)) * 1e4 + 1e6
    est = WindowedNonlinearShrinkageCovariance(window=W).fit(X)
    cov, _ = est._spectrum_inputs(est._state)
    expected = np.cov(X[-W:], rowvar=False, bias=True)
    assert np.allclose(cov, expected, rtol=1e-6), "rolling sums drifted from the truth"


def test_window_forgets_a_regime_the_expanding_estimator_remembers():
    from precise import WindowedNonlinearShrinkageCovariance

    W, p = 120, 8
    old, new = _bulk_cov(p, seed=1), _market_cov(p, seed=2)
    X = np.vstack([_draw(old, 600, seed=1), _draw(new, 600, seed=2)])

    windowed = WindowedNonlinearShrinkageCovariance(window=W).fit(X)
    expanding = NonlinearShrinkageCovariance().fit(X)
    # After a full window of the new regime, the window should describe it and nothing else.
    assert _rel_err(windowed.covariance_, new) < _rel_err(windowed.covariance_, old)
    assert _rel_err(windowed.covariance_, new) < _rel_err(expanding.covariance_, new)


def test_window_larger_than_the_stream_matches_the_expanding_estimator():
    from precise import WindowedNonlinearShrinkageCovariance

    X = _draw(_bulk_cov(6), 200)
    windowed = WindowedNonlinearShrinkageCovariance(window=10_000).fit(X)
    expanding = NonlinearShrinkageCovariance().fit(X)
    assert np.allclose(windowed.covariance_, expanding.covariance_, atol=1e-10)
