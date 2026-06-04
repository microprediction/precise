"""Correctness tests: do the estimators recover the right answer and behave as advertised?

Complements the contract checks in test_estimators.py (symmetry/PSD/invertibility) with
numerical-correctness, robustness, shrinkage, serialization, and edge-case tests. numpy only.
"""

import json

import numpy as np
import pytest

from precise import (
    AdaptiveEwaCovariance,
    DCCCovariance,
    EmpiricalCovariance,
    EwaCovariance,
    FactorCovariance,
    HuberCovariance,
    LedoitWolfCovariance,
    OASCovariance,
    ShrunkCovariance,
    TylerCovariance,
    all_estimators,
    keyed,
)


def _spd(n, rng):
    a = rng.standard_normal((n, n))
    return a @ a.T + n * np.eye(n)


# --------------------------------------------------------------- recovery
def test_empirical_recovers_true_covariance():
    rng = np.random.default_rng(0)
    true = _spd(4, rng)
    X = rng.multivariate_normal(np.zeros(4), true, size=50_000)
    est = EmpiricalCovariance().fit(X)
    # 50k samples -> sampling error is small; population cov should be close to truth.
    assert np.allclose(est.covariance_, true, rtol=0.05, atol=0.05)
    assert np.allclose(est.location_, X.mean(axis=0), atol=1e-8)


def test_ewa_tracks_a_regime_change():
    rng = np.random.default_rng(1)
    lo = rng.multivariate_normal([0, 0], [[1, 0], [0, 1]], size=3000)
    hi = rng.multivariate_normal([0, 0], [[9, 0], [0, 9]], size=3000)
    est = EwaCovariance(r=0.05)
    est.partial_fit(lo)
    var_lo = np.mean(np.diag(est.covariance_))
    est.partial_fit(hi)
    var_hi = np.mean(np.diag(est.covariance_))
    # The recency-weighted estimate should move from ~1 towards ~9 after the regime change.
    assert var_lo < 2.5
    assert var_hi > 5.0


def test_diff_matches_numpy_on_differences():
    rng = np.random.default_rng(2)
    X = np.cumsum(rng.standard_normal((1000, 3)), axis=0)  # integrated (random walk)
    est = EmpiricalCovariance(diff=True).fit(X)
    expected = np.cov(np.diff(X, axis=0), rowvar=False, bias=True)
    assert np.allclose(est.covariance_, expected, atol=1e-8)


# --------------------------------------------------------------- robustness
def test_huber_has_bounded_influence():
    # The defining property of a robust M-estimator: a single gross outlier moves the
    # estimate by a bounded amount, whereas a plain EWA update is moved without bound.
    rng = np.random.default_rng(3)
    true = np.array([[1.0, 0.5], [0.5, 1.0]])
    clean = rng.multivariate_normal([0, 0], true, size=3000)

    def influence_of_outlier(est):
        for row in clean:
            est.partial_fit(row)
        before = est.covariance_.copy()
        est.partial_fit(np.array([40.0, 40.0]))  # one gross outlier
        return np.linalg.norm(est.covariance_ - before)

    huber_move = influence_of_outlier(HuberCovariance(r=0.05, c=2.5))
    ewa_move = influence_of_outlier(EwaCovariance(r=0.05))
    # Huber should barely budge; EWA absorbs the full rank-one spike.
    assert huber_move < 0.1 * ewa_move, f"huber moved {huber_move:.3f}, ewa {ewa_move:.3f}"


# --------------------------------------------------------------- shrinkage
def test_ledoitwolf_shrinks_and_stays_well_conditioned():
    rng = np.random.default_rng(4)
    true = _spd(8, rng)
    X = rng.multivariate_normal(np.zeros(8), true, size=4000)
    lw = LedoitWolfCovariance(r=0.02)
    ewa = EwaCovariance(r=0.02)
    for row in X:
        lw.partial_fit(row)
        ewa.partial_fit(row)
    # shrinkage intensity is a probability
    assert 0.0 <= lw.get_state()["pi_bar"]  # tracked quantity is non-negative
    # shrinkage towards a scaled identity should not worsen conditioning
    cond_lw = np.linalg.cond(lw.covariance_)
    cond_ewa = np.linalg.cond(ewa.covariance_)
    assert cond_lw <= cond_ewa * 1.05


def test_oas_shrinks_toward_identity():
    rng = np.random.default_rng(40)
    true = _spd(8, rng)
    X = rng.multivariate_normal(np.zeros(8), true, size=4000)
    oas = OASCovariance(r=0.02)
    ewa = EwaCovariance(r=0.02)
    for row in X:
        oas.partial_fit(row)
        ewa.partial_fit(row)
    # Shrinkage towards a scaled identity should not worsen conditioning.
    assert np.linalg.cond(oas.covariance_) <= np.linalg.cond(ewa.covariance_) * 1.05


def test_shrunk_constant_correlation_preserves_variances():
    rng = np.random.default_rng(43)
    true = _spd(5, rng)
    X = rng.multivariate_normal(np.zeros(5), true, size=4000)
    shrunk = ShrunkCovariance(r=0.02, delta=0.5, target="constant_correlation")
    ewa = EwaCovariance(r=0.02)
    for row in X:
        shrunk.partial_fit(row)
        ewa.partial_fit(row)
    # The constant-correlation target preserves the diagonal (variances), only pulls correlations.
    assert np.allclose(np.diag(shrunk.covariance_), np.diag(ewa.covariance_), rtol=1e-6)
    assert np.min(np.linalg.eigvalsh(shrunk.covariance_)) > 0


def test_shrunk_identity_improves_conditioning():
    rng = np.random.default_rng(44)
    X = rng.multivariate_normal(np.zeros(8), _spd(8, rng), size=3000)
    shrunk = ShrunkCovariance(r=0.02, delta=0.3, target="identity").fit(X)
    ewa = EwaCovariance(r=0.02).fit(X)
    assert np.linalg.cond(shrunk.covariance_) <= np.linalg.cond(ewa.covariance_)


# --------------------------------------------------------------- adaptive
def test_adaptive_tracks_regime_change_better_than_a_slow_fixed_rate():
    # The point of adaptive forgetting: stay smooth (slow base rate) in calm periods, yet react
    # quickly to a regime change. Against a slow fixed rate, integrated tracking error through the
    # change should be lower. (A single end snapshot is the wrong metric for a noisier estimator.)
    rng = np.random.default_rng(45)
    calm = rng.multivariate_normal([0, 0], np.eye(2), size=3000)
    jump = rng.multivariate_normal([0, 0], 16 * np.eye(2), size=120)

    adaptive = AdaptiveEwaCovariance(r=0.01, max_r=0.3)  # slow base, adapts up on change
    fixed = EwaCovariance(r=0.01)  # same slow rate, no adaptation
    for est in (adaptive, fixed):
        est.partial_fit(calm)

    err_a, err_f = [], []
    for row in jump:
        adaptive.partial_fit(row)
        fixed.partial_fit(row)
        err_a.append(abs(np.mean(np.diag(adaptive.covariance_)) - 16.0))
        err_f.append(abs(np.mean(np.diag(fixed.covariance_)) - 16.0))
    assert np.mean(err_a) < np.mean(err_f)


# --------------------------------------------------------------- Tyler
def test_tyler_is_unit_diagonal_and_robust():
    rng = np.random.default_rng(46)
    corr = np.array([[1.0, 0.6], [0.6, 1.0]])
    clean = rng.multivariate_normal([0, 0], corr, size=4000)
    contaminated = clean.copy()
    mask = rng.random(len(clean)) < 0.05
    contaminated[mask] *= 30.0  # heavy outliers

    tyler = TylerCovariance(r=0.02)
    ewa = EwaCovariance(r=0.02)
    for row in contaminated:
        tyler.partial_fit(row)
        ewa.partial_fit(row)

    assert np.allclose(np.diag(tyler.covariance_), 1.0)  # reports a robust correlation
    err_tyler = abs(tyler.correlation_[0, 1] - 0.6)
    err_ewa = abs(ewa.correlation_[0, 1] - 0.6)
    assert err_tyler < err_ewa  # robust correlation resists the outliers


# --------------------------------------------------------------- DCC
def test_dcc_recovers_correlation_and_per_series_vol():
    rng = np.random.default_rng(41)
    vols = np.array([1.0, 3.0])
    corr = np.array([[1.0, 0.6], [0.6, 1.0]])
    cov = np.diag(vols) @ corr @ np.diag(vols)
    X = rng.multivariate_normal([0, 0], cov, size=40_000)
    est = DCCCovariance(r=0.01).fit(X)
    assert est.correlation_[0, 1] == pytest.approx(0.6, abs=0.1)
    assert np.allclose(np.diag(est.correlation_), 1.0)
    assert np.sqrt(np.diag(est.covariance_)) == pytest.approx(vols, rel=0.15)


# --------------------------------------------------------------- Factor
def test_factor_recovers_one_factor_structure():
    rng = np.random.default_rng(42)
    b = np.ones(4)  # single common factor with unit loadings
    f = rng.standard_normal(20_000)
    noise = 0.1 * rng.standard_normal((20_000, 4))
    X = np.outer(f, b) + noise  # true cov ~ b bᵀ + 0.01 I  (rank-1 + diagonal)
    est = FactorCovariance(k=1, r=0.01).fit(X)
    C = est.covariance_
    off = C[0, 1]
    assert off == pytest.approx(1.0, abs=0.3)  # off-diagonals driven by the common factor
    assert np.min(np.linalg.eigvalsh(C)) > 0


# --------------------------------------------------------------- scoring
def test_score_matches_analytic_gaussian_loglik():
    rng = np.random.default_rng(5)
    X = rng.multivariate_normal([0, 0, 0], _spd(3, rng), size=3000)
    est = EmpiricalCovariance().fit(X)
    test = rng.standard_normal((10, 3))
    prec = est.precision_
    _, logdet = np.linalg.slogdet(prec)
    centered = test - est.location_
    quad = np.einsum("ij,jk,ik->i", centered, prec, centered)
    manual = np.mean(0.5 * logdet - 0.5 * quad - 0.5 * 3 * np.log(2 * np.pi))
    assert est.score(test) == pytest.approx(manual, rel=1e-10)


def test_mahalanobis_matches_manual():
    rng = np.random.default_rng(6)
    X = rng.multivariate_normal([0, 0], _spd(2, rng), size=2000)
    est = EmpiricalCovariance().fit(X)
    pts = rng.standard_normal((5, 2))
    d = pts - est.location_
    manual = np.einsum("ij,jk,ik->i", d, est.precision_, d)
    assert np.allclose(est.mahalanobis(pts), manual)


# --------------------------------------------------------------- serialization
@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_get_state_is_real_json(Est):
    rng = np.random.default_rng(7)
    X = rng.standard_normal((300, 4))
    est = Est().fit(X)
    # Actually serialize to a JSON string and restore through a fresh instance.
    blob = json.dumps(est.get_state())
    restored = Est().set_state(json.loads(blob))
    assert np.allclose(restored.covariance_, est.covariance_, atol=1e-12)
    assert np.allclose(restored.location_, est.location_, atol=1e-12)


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_sklearn_style_params_roundtrip(Est):
    est = Est()
    params = est.get_params()
    clone = type(est)(**params)  # the get_params/clone idiom used by the keyed adapters
    assert clone.get_params() == params


# --------------------------------------------------------------- determinism
@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_deterministic(Est):
    X = np.random.default_rng(8).standard_normal((500, 3))
    assert np.allclose(Est().fit(X).covariance_, Est().fit(X).covariance_)


# --------------------------------------------------------------- edge cases
@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_single_dimension(Est):
    rng = np.random.default_rng(9)
    X = rng.standard_normal((400, 1)) * 2.0
    est = Est().fit(X)
    assert est.covariance_.shape == (1, 1)
    assert est.covariance_[0, 0] > 0


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_constant_feature_does_not_crash(Est):
    rng = np.random.default_rng(10)
    X = rng.standard_normal((400, 3))
    X[:, 1] = 5.0  # a zero-variance column
    est = Est().fit(X)
    C = est.covariance_
    assert np.all(np.isfinite(C))
    assert np.all(np.isfinite(est.correlation_))  # must not divide-by-zero to nan/inf
    assert np.all(np.isfinite(est.precision_))  # try_invert must fall back gracefully


def test_unfitted_raises():
    from precise.base import NotFittedError

    with pytest.raises(NotFittedError):
        _ = EmpiricalCovariance().covariance_


# --------------------------------------------------------------- keyed adapters
def test_dynamic_universe_bounds_and_evicts():
    rng = np.random.default_rng(11)
    d = keyed(EmpiricalCovariance(), dynamic=True, max_universes=3, max_staleness=5)
    # feed many distinct key-sets; the number of universes must stay bounded
    for i in range(200):
        keys = [f"k{j}" for j in range(i % 6, i % 6 + 3)]
        d.update({k: float(rng.standard_normal()) for k in keys})
    assert len(d.states) <= 3


def test_fixed_universe_impute_modes_agree_when_complete():
    rng = np.random.default_rng(12)
    rows = rng.standard_normal((300, 3))
    cov_by_mode = {}
    for mode in ("ffill", "mean", "zero"):
        k = keyed(EmpiricalCovariance(), impute=mode)
        for r in rows:
            k.update({"A": r[0], "B": r[1], "C": r[2]})
        cov_by_mode[mode] = k.get_cov(["A", "B", "C"])
    # With no missing keys, imputation never triggers, so all modes must agree exactly.
    assert np.allclose(cov_by_mode["ffill"], cov_by_mode["mean"])
    assert np.allclose(cov_by_mode["ffill"], cov_by_mode["zero"])


# --------------------------------------------------------------- linalg safety nets
def test_nearest_pos_def_repairs_indefinite_matrix():
    from precise._linalg import is_positive_def, nearest_pos_def

    a = np.array([[1.0, 2.0], [2.0, 1.0]])  # eigenvalues 3 and -1 -> indefinite
    assert not is_positive_def(a)
    fixed = nearest_pos_def(a)
    assert is_positive_def(fixed)
    assert np.allclose(fixed, fixed.T)


def test_try_invert_falls_back_on_singular():
    from precise._linalg import try_invert

    singular = np.array([[1.0, 1.0], [1.0, 1.0]])  # rank 1, not invertible
    inv = try_invert(singular)
    assert np.all(np.isfinite(inv))  # pseudo-inverse / ridge fallback, not a crash


def test_as_rows_rejects_3d():
    from precise._conventions import as_rows

    with pytest.raises(ValueError):
        as_rows(np.zeros((2, 2, 2)))


def test_keyed_matches_positional_estimator_exactly():
    rng = np.random.default_rng(13)
    rows = rng.standard_normal((400, 3))
    pos = EmpiricalCovariance().fit(rows)
    k = keyed(EmpiricalCovariance())
    for r in rows:
        k.update({"A": r[0], "B": r[1], "C": r[2]})
    assert np.allclose(k.get_cov(["A", "B", "C"]), pos.covariance_, atol=1e-10)
