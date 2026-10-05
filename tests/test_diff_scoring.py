"""With diff=True, score and mahalanobis must take the same input as fit: levels.

``fit`` differenced its levels but ``score`` and ``mahalanobis`` applied the difference model
straight to the levels they were given. Two level panels with identical differences fitted the same
model yet scored -1.4e4 and -2.0e12, and shifting price origins reversed the ranking of a full
against a diagonal covariance. (#105)
"""

import numpy as np
import pytest

from precise import DiagonalCovariance, EmpiricalCovariance, all_estimators


def _levels(n=500, seed=12):
    rng = np.random.default_rng(seed)
    C = np.array([[1.0, 0.4], [0.4, 2.0]])
    steps = rng.multivariate_normal([0.01, -0.02], C, size=n)
    return np.array([100.0, 200.0]) + np.cumsum(steps, axis=0)


def _gaussian_score(X, mean, cov):
    centered = X - mean
    prec = np.linalg.inv(cov)
    quad = np.einsum("ij,jk,ik->i", centered, prec, centered)
    _, logdet = np.linalg.slogdet(cov)
    return float(np.mean(-0.5 * (logdet + quad + X.shape[1] * np.log(2 * np.pi))))


def test_score_of_levels_is_the_gaussian_score_of_their_differences():
    levels = _levels()
    est = EmpiricalCovariance(diff=True).fit(levels)
    d = np.diff(levels, axis=0)
    manual = _gaussian_score(d, d.mean(axis=0), np.cov(d.T, bias=True))
    assert est.score(levels) == pytest.approx(manual, rel=1e-10)
    centered = d - d.mean(axis=0)
    manual_m = np.einsum("ij,jk,ik->i", centered, np.linalg.inv(np.cov(d.T, bias=True)), centered)
    assert np.allclose(est.mahalanobis(levels), manual_m)


def test_panels_with_identical_differences_score_identically():
    # The issue's reproduction: same differences, same model, scores of -1.4e4 and -2.0e12.
    levels = _levels()
    shift = np.array([1_000_000.0, -2_000_000.0])
    a = EmpiricalCovariance(diff=True).fit(levels)
    b = EmpiricalCovariance(diff=True).fit(levels + shift)
    assert a.score(levels) == pytest.approx(b.score(levels + shift), rel=1e-8)


@pytest.mark.parametrize("Est", all_estimators(), ids=lambda e: e.__name__)
def test_shifting_the_price_origin_does_not_change_the_score(Est):
    if "diff" not in Est().get_params():
        pytest.skip("no diff parameter")
    est = Est(diff=True).fit(_levels())
    test = _levels(n=50, seed=13)
    shift = np.array([1_000_000.0, -2_000_000.0])
    assert est.score(test) == pytest.approx(est.score(test + shift), rel=1e-8)
    assert np.allclose(est.mahalanobis(test), est.mahalanobis(test + shift), rtol=1e-6)


def test_price_origins_cannot_reverse_a_model_ranking():
    rng = np.random.default_rng(3)
    C = np.array([[1.0, 0.9], [0.9, 1.0]])
    levels = np.cumsum(rng.multivariate_normal([0, 0], C, size=800), axis=0)
    train, test = levels[:600], levels[600:]
    shift = np.array([1e6, -1e6])
    full = EmpiricalCovariance(diff=True).fit(train)
    diag = DiagonalCovariance(diff=True).fit(train)
    assert full.score(test) > diag.score(test)
    assert full.score(test + shift) > diag.score(test + shift)


def test_one_level_row_cannot_be_scored_with_diff():
    est = EmpiricalCovariance(diff=True).fit(_levels())
    with pytest.raises(ValueError, match="at least two consecutive rows"):
        est.score(_levels()[0])
    with pytest.raises(ValueError, match="at least two consecutive rows"):
        est.mahalanobis(_levels()[:1])
    assert est.mahalanobis(_levels()[:2]).shape == (1,)
