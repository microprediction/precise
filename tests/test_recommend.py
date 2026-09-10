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


def test_trained_model_ships_and_is_used():
    from precise import recommend

    assert recommend._MODEL is not None  # frozen decision tree ships with the package
    rng = np.random.default_rng(5)
    out = suggest(rng.standard_normal((80, 20)), top=3)
    assert len(out) == 3
    assert all(issubclass(c, BaseOnlineCovariance) for c in out)


def test_heavy_tails_raise_the_robust_estimators_in_the_heuristic():
    # The ruleset's contract is that excess kurtosis promotes Huber and Tyler. It does not promote
    # them above everything: the low-dimensional branch adds more (+2.0) than the heavy-tail branch
    # (+1.5), so on small well-conditioned data Empirical still outranks them.
    #
    # suggest() no longer returns them here at all, and that is a deliberate change. The trained
    # model outranks the heuristic and disagrees: measured on this data under GMV, the metric the
    # model is trained against, Tyler places 5th of 20 and Huber 15th. Part of Tyler's
    # disadvantage is structural, since it estimates a correlation while GMV scores a covariance.
    from precise.recommend import _scores

    rng = np.random.default_rng(3)
    light = rng.standard_normal((1500, 4))
    heavy = light * np.sqrt(3.0 / rng.chisquare(3, size=(1500, 1)))
    assert covariance_features(heavy)["avg_excess_kurtosis"] > 1.0 > covariance_features(light)[
        "avg_excess_kurtosis"
    ]

    for name in ("HuberCovariance", "TylerCovariance"):
        bump = _scores(covariance_features(heavy))[name] - _scores(covariance_features(light))[name]
        assert bump > 0, f"heavy tails must promote {name}"


def test_frozen_model_is_not_degenerate():
    # Regression guard. An earlier exporter cast sklearn's class *proportions* with int(), which
    # floors everything under 1.0 to zero: 46 of 47 nodes carried no weight, so the trained model
    # contributed nothing and suggest() silently ran on the heuristic ruleset alone. Nothing failed
    # loudly, which is why this is a test.
    from precise import _recommender_model as model

    carrying = [row for row in model.VALUE if any(row)]
    assert len(carrying) > 0.5 * len(model.VALUE), (
        f"only {len(carrying)} of {len(model.VALUE)} nodes carry weight; the model is empty"
    )
    assert max(sum(row) for row in model.VALUE) > 1, "leaf weights look like truncated fractions"


def test_frozen_model_needs_no_numpy():
    # It is imported by precise/__init__ and must stay plain Python. numpy 2 reprs numpy scalars
    # as np.str_('...'), which once leaked into the generated CLASSES and broke `import precise`
    # with a NameError -- not an ImportError, so the guard in recommend.py did not catch it.
    from pathlib import Path

    import precise._recommender_model as model

    src = Path(model.__file__).read_text()
    assert "np." not in src and "numpy" not in src
    assert all(type(c) is str for c in model.CLASSES)


def test_the_model_covers_most_of_the_registry():
    # The bug this guards against was a model naming 9 of 20 estimators, so eleven could never be
    # returned however suitable. Exhaustive coverage is the wrong bar: an estimator that wins no
    # problem under the assessor should not be recommended, and the labels are what they are.
    # What matters is that the model spans the registry rather than a corner of it.
    from precise import _recommender_model as model
    from precise import estimator_names

    registry = set(estimator_names())
    assert set(model.CLASSES) <= registry, "model names an estimator that is not registered"
    assert len(model.CLASSES) >= 0.75 * len(registry), (
        f"only {len(model.CLASSES)} of {len(registry)} estimators are reachable: "
        f"{sorted(registry - set(model.CLASSES))}"
    )
    # The nonlinear shrinkers do win problems, so an export that dropped them would be a defect.
    for name in ("NonlinearShrinkageCovariance", "WindowedNonlinearShrinkageCovariance",
                 "EwaNonlinearShrinkageCovariance"):
        assert name in model.CLASSES


def test_suggestions_respond_to_the_data():
    # A model returning the same three estimators for everything is indistinguishable from no
    # model, which is what the degenerate export amounted to. The low-dimensional case needs
    # genuine off-diagonal structure: against independent columns the truth really is diagonal,
    # and DiagonalCovariance is then the right answer rather than a symptom.
    from precise import suggest

    rng = np.random.default_rng(11)
    loadings = rng.standard_normal((8, 3))
    cov = loadings @ loadings.T + np.diag(0.3 + 0.4 * rng.random(8))
    rich = suggest(rng.multivariate_normal(np.zeros(8), cov, 400), top=3)

    big = rng.standard_normal((60, 60))
    scarce = suggest(
        rng.multivariate_normal(np.zeros(60), big @ big.T / 60 + np.eye(60), 45), top=3
    )

    assert rich != scarce
    assert rich[0].__name__ == "EmpiricalCovariance", "plenty of data, few variables"
    assert scarce[0].__name__ != "EmpiricalCovariance", "p > n needs regularization"
