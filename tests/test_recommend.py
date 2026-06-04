"""Tests for the feature extractor and the suggest() recommender."""

import numpy as np

from precise import BaseOnlineCovariance, covariance_features, suggest


def _factor_data(n, p, rng):
    # low-rank (factor) structure -> high effective concentration
    loadings = rng.standard_normal((p, 2))
    f = rng.standard_normal((n, 2))
    return f @ loadings.T + 0.3 * rng.standard_normal((n, p))


def test_features_are_observable_and_sane():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((500, 6))
    f = covariance_features(X)
    assert f["n"] == 500 and f["p"] == 6
    assert f["p_over_n"] == 6 / 500
    assert 1.0 <= f["effective_rank"] <= 6.0
    assert 0.0 < f["sphericity"] <= 1.0
    assert f["condition_number"] >= 1.0


def test_suggest_returns_estimator_classes():
    rng = np.random.default_rng(1)
    X = rng.standard_normal((400, 5))
    out = suggest(X, top=3)
    assert len(out) == 3
    assert all(isinstance(c, type) and issubclass(c, BaseOnlineCovariance) for c in out)


def test_high_dimensional_prefers_shrinkage_or_factor():
    rng = np.random.default_rng(2)
    X = _factor_data(n=60, p=40, rng=rng)  # p/n large + low-rank
    names = [c.__name__ for c in suggest(X, top=4)]
    assert any(n in names for n in
               ("FactorCovariance", "LedoitWolfCovariance", "OASCovariance",
                "ShrunkCovariance", "SchurCovariance"))
    assert "EmpiricalCovariance" not in names[:2]  # the naive estimator is not top-ranked here


def test_heavy_tailed_prefers_robust():
    rng = np.random.default_rng(3)
    # heavy tails: Student-t with low dof
    g = rng.standard_normal((1500, 4))
    scale = np.sqrt(3.0 / rng.chisquare(3, size=(1500, 1)))
    X = g * scale
    names = [c.__name__ for c in suggest(X, top=4)]
    assert any(n in names for n in ("HuberCovariance", "TylerCovariance"))
