"""Bake-off: score every registered online covariance estimator against known ground truth.

Builds a suite of *discriminating* scenarios — each designed so a different family of estimators
should win — samples data, streams it through every estimator in ``precise.all_estimators()``, and
scores recovery. Prints a leaderboard plus the winner of each scenario.

This is the cleaner reincarnation of the old elo bake-off, against the new estimator contract. It
runs out of the box on a numpy ground-truth generator; if the sibling
[`randomcov`](https://github.com/microprediction/randomcov) package is installed
(``pip install precise[research]``) it adds richer generated structures.

The primary, fair metric is **correlation error** (scale-invariant, so it is fair to the
correlation-only estimators such as Tyler). ``cov_err`` (relative covariance error) and ``nll``
(negative held-out log-likelihood, clipped) are shown as secondary columns.

    python research/bakeoff.py
"""

from __future__ import annotations

import numpy as np

from precise import all_estimators

try:
    from randomcov import random_covariance_matrix

    HAVE_RANDOMCOV = True
except ImportError:  # pragma: no cover - exercised only when randomcov is installed
    HAVE_RANDOMCOV = False

_NLL_CLIP = 1e3


# ----------------------------------------------------------------- ground-truth covariances
def _equicorrelation(n, rho=0.6):
    c = np.full((n, n), rho)
    np.fill_diagonal(c, 1.0)
    return c


def _one_factor(n, rng):
    b = rng.uniform(0.5, 1.5, size=n)
    return np.outer(b, b) + np.diag(rng.uniform(0.2, 1.0, size=n))


def _three_factor(n, rng):
    B = rng.standard_normal((n, 3))
    return B @ B.T + np.diag(rng.uniform(0.2, 1.0, size=n))


def _ar1_toeplitz(n, rho=0.7):
    idx = np.arange(n)
    return rho ** np.abs(idx[:, None] - idx[None, :])


def _correlation(cov):
    d = np.sqrt(np.maximum(np.diag(cov), 1e-12))
    return cov / np.outer(d, d)


def _gaussian(cov, n, rng):
    return rng.multivariate_normal(np.zeros(len(cov)), cov, size=n)


def _heavy_tailed(cov, n, rng, df=5):
    # Multivariate Student-t scaled to have covariance == cov (fat tails, finite variance).
    z = rng.multivariate_normal(np.zeros(len(cov)), cov * (df - 2) / df, size=n)
    return z * np.sqrt(df / rng.chisquare(df, size=(n, 1)))


# ----------------------------------------------------------------- discriminating scenarios
def build_scenarios(d=12, n=1500, n_test=500, seed=0):
    """Yield (name, train, test, true_cov), each tuned to favour a different estimator family."""
    rng = np.random.default_rng(seed)
    scs = []

    # Stationary structural (the well-conditioned baseline; the empirical estimator should do well).
    for name, cov in [
        ("equicorr", _equicorrelation(d)),
        ("one_factor", _one_factor(d, rng)),
        ("ar1_toeplitz", _ar1_toeplitz(d)),
    ]:
        scs.append((name, _gaussian(cov, n, rng), _gaussian(cov, n_test, rng), cov))

    # High dimension, few samples: shrinkage / factor structure should help.
    dh = 40
    cov = _one_factor(dh, rng)
    scs.append(("high_dim_low_n", _gaussian(cov, 60, rng), _gaussian(cov, n_test, rng), cov))

    # Regime change: correlation jumps halfway; recency-weighted estimators should track it.
    a, b = _equicorrelation(d, 0.2), _equicorrelation(d, 0.85)
    train = np.vstack([_gaussian(a, n // 2, rng), _gaussian(b, n // 2, rng)])
    scs.append(("regime_change", train, _gaussian(b, n_test, rng), b))

    # Gross outliers: 5% of rows replaced by large *independent* noise (which destroys the
    # correlation structure). Robust estimators should preserve it; the empirical one should not.
    cov = _one_factor(d, rng)
    tr = _gaussian(cov, n, rng)
    mask = rng.random(len(tr)) < 0.05
    tr[mask] = rng.standard_normal((int(mask.sum()), d)) * 8.0
    scs.append(("contaminated", tr, _gaussian(cov, n_test, rng), cov))

    # Heavy tails (elliptical): robust / Tyler should hold up.
    cov = _three_factor(d, rng)
    scs.append(("heavy_tailed", _heavy_tailed(cov, n, rng), _heavy_tailed(cov, n_test, rng), cov))

    if HAVE_RANDOMCOV:
        for method in ("lkj", "wishart", "residuals"):
            try:
                cov = np.asarray(random_covariance_matrix(n=d, corr_method=method))
                tr, te = _gaussian(cov, n, rng), _gaussian(cov, n_test, rng)
                scs.append((f"randomcov_{method}", tr, te, cov))
            except Exception:  # pragma: no cover - depends on randomcov internals
                pass
    return scs


# ----------------------------------------------------------------- run + score
def run(**kwargs):
    """Return ``{estimator_name: {scenario_name: {metric: value}}}``."""
    scs = build_scenarios(**kwargs)
    results: dict = {Est.__name__: {} for Est in all_estimators()}
    for name, train, test, true_cov in scs:
        true_corr = _correlation(true_cov)
        for Est in all_estimators():
            est = Est().fit(train)
            corr_err = np.linalg.norm(est.correlation_ - true_corr) / np.linalg.norm(true_corr)
            cov_err = np.linalg.norm(est.covariance_ - true_cov) / np.linalg.norm(true_cov)
            try:
                nll = float(np.clip(-est.score(test), -_NLL_CLIP, _NLL_CLIP))
            except Exception:
                nll = _NLL_CLIP
            results[Est.__name__][name] = {"corr_err": corr_err, "cov_err": cov_err, "nll": nll}
    return results


def _mean(results, name, metric):
    vals = [m[metric] for m in results[name].values() if np.isfinite(m[metric])]
    return float(np.mean(vals)) if vals else float("inf")


def leaderboard(results) -> str:
    names = list(results)
    cells = list(next(iter(results.values())))
    # Rank by the fair, scale-invariant correlation error within each scenario, then average.
    ranks = {nm: [] for nm in names}
    for key in cells:
        order = sorted(names, key=lambda nm: results[nm][key]["corr_err"])
        for rank, nm in enumerate(order):
            ranks[nm].append(rank + 1)
    avg_rank = {nm: float(np.mean(ranks[nm])) for nm in names}

    lines = [
        f"{'estimator':26}{'avg_corr_rank':>14}{'corr_err':>10}{'cov_err':>10}{'nll':>9}",
        "-" * 69,
    ]
    for nm in sorted(names, key=lambda n: avg_rank[n]):
        lines.append(
            f"{nm:26}{avg_rank[nm]:>14.2f}{_mean(results, nm, 'corr_err'):>10.3f}"
            f"{_mean(results, nm, 'cov_err'):>10.3f}{_mean(results, nm, 'nll'):>9.2f}"
        )
    return "\n".join(lines)


def per_scenario_winners(results) -> str:
    cells = list(next(iter(results.values())))
    lines = ["", "Winner (lowest corr_err) per scenario:", "-" * 50]
    for key in cells:
        best = min(results, key=lambda nm: results[nm][key]["corr_err"])
        lines.append(f"  {key:24} -> {best}")
    return "\n".join(lines)


if __name__ == "__main__":
    src = "randomcov + numpy" if HAVE_RANDOMCOV else "numpy fallback"
    print(f"precise bake-off  [{len(all_estimators())} estimators, ground truth: {src}]\n")
    res = run()
    print(leaderboard(res))
    print(per_scenario_winners(res))
