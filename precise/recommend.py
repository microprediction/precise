"""Recommend an online covariance estimator from observable properties of the data.

The covariance analogue of humpday's ``suggest`` — features computed from the *sample* (never the
unknown truth) drive a recommendation of which estimator to use. The motivating evidence
(``research/bakeoff.py``) is that no single estimator wins everywhere: the empirical estimator is
best on clean, low-dimensional data; shrinkage / factor estimators win when ``p`` is large relative
to the sample; robust estimators win under heavy tails. ``suggest`` harvests that regime-dependence.

The ruleset below is a transparent, frozen heuristic (v0) — the place a *trained* recommender,
fitted out-of-sample over generated ensembles in ``research/``, will eventually slot in.
"""

from __future__ import annotations

from types import ModuleType

import numpy as np

from precise._conventions import as_rows
from precise.registry import all_estimators

# A frozen decision tree trained offline (research/train_recommender.py); numpy-only to walk.
try:
    import precise._recommender_model as _loaded
    _MODEL: ModuleType | None = _loaded
except ImportError:  # pragma: no cover - model is optional
    _MODEL = None


def covariance_features(X) -> dict:
    """Observable descriptors of a data window ``X`` (n_samples x n_features).

    All computed from the sample — usable without knowing the true covariance.
    """
    rows = as_rows(X)
    n, p = rows.shape
    S = np.atleast_2d(np.cov(rows, rowvar=False, bias=True))
    evals = np.clip(np.linalg.eigvalsh(S), 1e-12, None)
    total = float(evals.sum())
    eff_rank = (total**2) / float(np.sum(evals**2)) if total > 0 else 1.0  # participation ratio
    var = np.clip(np.diag(S), 1e-12, None)
    corr = S / np.sqrt(np.outer(var, var))
    off = corr[~np.eye(p, dtype=bool)] if p > 1 else np.array([0.0])
    centered = rows - rows.mean(axis=0)
    m4 = np.mean(centered**4, axis=0)
    excess_kurt = np.mean(m4 / np.clip(var, 1e-12, None) ** 2 - 3.0)
    return {
        "n": int(n),
        "p": int(p),
        "p_over_n": p / n,
        "effective_rank": float(eff_rank),
        "sphericity": float(eff_rank / p),  # 1 = isotropic, small = spiked
        "condition_number": float(evals.max() / evals.min()),
        "mean_abs_offdiag_corr": float(np.mean(np.abs(off))),
        "avg_excess_kurtosis": float(excess_kurt),
    }


def _scores(features: dict) -> dict:
    """Frozen heuristic ruleset: estimator name -> preference score (higher = recommend)."""
    score = {cls.__name__: 0.0 for cls in all_estimators()}
    high_dim = features["p_over_n"] > 0.25 or features["sphericity"] < 0.6
    ill_conditioned = features["condition_number"] > 50.0
    heavy_tailed = features["avg_excess_kurtosis"] > 1.0

    if high_dim or ill_conditioned:
        for nm in ("FactorCovariance", "LedoitWolfCovariance", "OASCovariance",
                   "ShrunkCovariance", "SchurCovariance"):
            score[nm] += 2.0
    else:
        for nm in ("EmpiricalCovariance", "EwaCovariance"):
            score[nm] += 2.0

    if heavy_tailed:
        for nm in ("HuberCovariance", "TylerCovariance"):
            score[nm] += 1.5

    score["LedoitWolfCovariance"] += 0.5  # strong, safe default tie-breaker
    return score


def _trained_weights(features: dict) -> dict:
    """Walk the frozen decision tree (numpy only) → {estimator_name: leaf class count}."""
    assert _MODEL is not None
    x = np.asarray([features[k] for k in _MODEL.FEATURES])
    xs = (x - np.asarray(_MODEL.MEAN)) / np.asarray(_MODEL.STD)
    feat = _MODEL.FEATURE
    node = 0
    while feat[node] != -2:  # -2 marks a leaf
        node = _MODEL.LEFT[node] if xs[feat[node]] <= _MODEL.THRESHOLD[node] else _MODEL.RIGHT[node]
    counts = _MODEL.VALUE[node]
    return {cls: counts[i] for i, cls in enumerate(_MODEL.CLASSES)}


def suggest(X, top: int = 3) -> list:
    """Recommend estimator classes for data ``X``, best first.

        from precise import suggest
        for Est in suggest(returns):
            est = Est(); ...

    Uses the frozen trained recommender (a decision tree over :func:`covariance_features`, fitted
    offline in ``research/train_recommender.py``) when present, breaking ties with the heuristic
    ruleset; otherwise falls back to the heuristic alone. Returns the top-``top``
    :class:`~precise.base.BaseOnlineCovariance` subclasses.
    """
    features = covariance_features(X)
    heuristic = _scores(features)
    if _MODEL is not None:
        weights = _trained_weights(features)
        ranked = sorted(
            all_estimators(),
            key=lambda cls: (-weights.get(cls.__name__, 0), -heuristic[cls.__name__]),
        )
    else:
        ranked = sorted(all_estimators(), key=lambda cls: -heuristic[cls.__name__])
    return ranked[:top]
