"""Out-of-sample validation of the estimator recommender.

The bar for the recommender (``precise.suggest``): does choosing an estimator per-problem, from
observable sample features, beat the best *single* fixed estimator — out of sample, on problem
families it was not tuned on? We measure the **average rank** of the chosen estimator per trial
(1 = the per-trial oracle / best estimator under a held-out assessor); lower is better. Ranks are
robust to the score blow-ups that ill-conditioned estimates produce.

Protocol — **leave-one-ensemble-out**: for each generative family, pick the best fixed estimator on
the *other* families, then evaluate the recommender and that fixed estimator on the held-out family.
Because the conclusions are sensitive to the generating ensemble (see
``papers/evaluation_and_generation_review.md``), this cross-ensemble design is the synthetic half of
the proof; a real-equity-data holdout is the other half.

Estimates are judged with the minimum-variance assessor by default — scale-invariant, bounded, and
the literature's economic standard — never the full likelihood. Runs on numpy ensembles out of the
box; richer with ``randomcov``.

    python research/oos.py
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from precise import all_estimators, suggest
from precise.assessment import GMVVariance

try:
    from randomcov import random_covariance_matrix

    HAVE_RANDOMCOV = True
except ImportError:  # pragma: no cover
    HAVE_RANDOMCOV = False


# --------------------------------------------------------------- generative ensembles
def _equicorr(p, rng):
    c = np.full((p, p), 0.6)
    np.fill_diagonal(c, 1.0)
    return c


def _one_factor(p, rng):
    b = rng.uniform(0.5, 1.5, p)
    return np.outer(b, b) + np.diag(rng.uniform(0.2, 1.0, p))


def _three_factor(p, rng):
    B = rng.standard_normal((p, 3))
    return B @ B.T + np.diag(rng.uniform(0.2, 1.0, p))


def _ar1(p, rng):
    idx = np.arange(p)
    return 0.7 ** np.abs(idx[:, None] - idx[None, :])


def _spiked(p, rng):
    spikes = np.concatenate([rng.uniform(8, 15, 3), np.full(p - 3, 0.4)])
    Q, _ = np.linalg.qr(rng.standard_normal((p, p)))
    return (Q * spikes) @ Q.T


def _diag_hetero(p, rng):
    return np.diag(rng.uniform(0.1, 5.0, p))


# (generator, heavy_tailed?)
ENSEMBLES = {
    "equicorr": (_equicorr, False),
    "one_factor": (_one_factor, False),
    "three_factor": (_three_factor, False),
    "ar1_toeplitz": (_ar1, False),
    "spiked": (_spiked, False),
    "diag_hetero": (_diag_hetero, False),
    "one_factor_heavy": (_one_factor, True),
    "ar1_heavy": (_ar1, True),
}
if HAVE_RANDOMCOV:  # pragma: no cover
    for _m in ("lkj", "wishart", "residuals"):
        ENSEMBLES[f"randomcov_{_m}"] = (
            (lambda p, rng, m=_m: np.asarray(random_covariance_matrix(n=p, corr_method=m))),
            False,
        )


def _sample(cov, n, rng, heavy):
    if not heavy:
        return rng.multivariate_normal(np.zeros(len(cov)), cov, size=n)
    df = 5
    z = rng.multivariate_normal(np.zeros(len(cov)), cov * (df - 2) / df, size=n)
    return z * np.sqrt(df / rng.chisquare(df, size=(n, 1)))


# --------------------------------------------------------------- one trial
def _ranks(scores: dict) -> dict:
    """Map estimator -> rank (1 = best), higher score is better."""
    order = sorted(scores, key=lambda k: -scores[k])
    return {nm: i + 1 for i, nm in enumerate(order)}


def _trial(gen, heavy, p, n_train, n_test, rng, assessor, recommender=None):
    """One trial: score every estimator OOS, and record the recommended one.

    ``recommender`` is a callable ``train_window -> estimator_name``; when ``None`` the shipped
    :func:`precise.suggest` (frozen tree) is used. Passing a freshly-trained predictor is what makes
    :func:`leave_one_family_out_trained` leak-free.
    """
    true_cov = gen(p, rng)
    train = _sample(true_cov, n_train, rng, heavy)
    test = _sample(true_cov, n_test, rng, heavy)
    scores = {}
    for cls in all_estimators():
        try:
            scores[cls.__name__] = assessor.score(cls().fit(train).covariance_, X_test=test)
        except Exception:
            scores[cls.__name__] = -np.inf
    if recommender is not None:
        recommended = recommender(train)
    else:
        recommended = suggest(train, top=1)[0].__name__
    return scores, recommended


def _best_fixed(train_ensembles, p, n_train, n_test, trials, rng, assessor):
    """The estimator with the best mean rank across the training ensembles."""
    accum = defaultdict(list)
    names = list(train_ensembles)
    for _ in range(trials):
        gen, heavy = ENSEMBLES[names[rng.integers(len(names))]]
        scores, _ = _trial(gen, heavy, p, n_train, n_test, rng, assessor)
        for k, r in _ranks(scores).items():
            accum[k].append(r)
    return min(accum, key=lambda k: np.mean(accum[k]))


def leave_one_ensemble_out(p=30, n_train=60, n_test=300, trials=40, seed=0, assessor=None):
    """Return ``{held_out: {best_fixed, rank_recommender, rank_best_fixed}}`` (rank 1 = best)."""
    assessor = assessor or GMVVariance()
    rng = np.random.default_rng(seed)
    names = list(ENSEMBLES)
    results = {}
    for held in names:
        train_ens = [e for e in names if e != held]
        bf = _best_fixed(train_ens, p, n_train, n_test, trials, rng, assessor)
        gen, heavy = ENSEMBLES[held]
        rk_rec, rk_bf = [], []
        for _ in range(trials):
            scores, rec = _trial(gen, heavy, p, n_train, n_test, rng, assessor)
            ranks = _ranks(scores)
            rk_rec.append(ranks[rec])
            rk_bf.append(ranks[bf])
        results[held] = {
            "best_fixed": bf,
            "rank_recommender": float(np.mean(rk_rec)),
            "rank_best_fixed": float(np.mean(rk_bf)),
        }
    return results


def _train_recommender(train_ensembles, n_problems, rng, assessor):
    """Fit a *fresh* decision tree on ``train_ensembles`` only; return ``predict(window)->name``.

    Mirrors the shipped pipeline (``research/train_recommender.py``: same features, same tree
    hyper-parameters) but is restricted to a subset of generative families, so the resulting
    recommender has *never seen* the held-out family. Requires scikit-learn (research extra).
    """
    from sklearn.tree import DecisionTreeClassifier

    from research.train_recommender import _features

    ests = all_estimators()
    names = [E.__name__ for E in ests]
    Xf, y = [], []
    for _ in range(n_problems):
        gen, heavy = ENSEMBLES[train_ensembles[rng.integers(len(train_ensembles))]]
        p = int(rng.choice([15, 25, 40, 60]))
        n = max(int(p * rng.choice([0.5, 0.8, 1.5, 3.0])), 10)
        true = gen(p, rng)
        tr, te = _sample(true, n, rng, heavy), _sample(true, 400, rng, heavy)
        scores = []
        for E in ests:
            try:
                scores.append(assessor.score(E().fit(tr).covariance_, X_test=te))
            except Exception:
                scores.append(-np.inf)
        Xf.append(_features(tr))
        y.append(names[int(np.argmax(scores))])
    X = np.asarray(Xf, dtype=float)
    mean, std = X.mean(0), X.std(0) + 1e-9
    # hyper-parameters mirror research/train_recommender.main
    clf = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10, random_state=0)
    clf.fit((X - mean) / std, y)

    def predict(window):
        f = (np.asarray(_features(window), dtype=float) - mean) / std
        return str(clf.predict(f[None, :])[0])

    return predict


def leave_one_family_out_trained(
    p=30, n_train=60, n_test=300, trials=40, n_problems=500, seed=0, assessor=None
):
    """Leak-free LOFO for the *trained* recommender.

    For each held-out generative family, train a brand-new tree on the *other* families only, then
    evaluate its per-problem picks on the held-out family — so the recommender is judged purely on
    its ability to generalize to a generative regime it never saw during training (the gap the
    shipped frozen model, trained on all families, cannot itself demonstrate).
    """
    assessor = assessor or GMVVariance()
    rng = np.random.default_rng(seed)
    names = list(ENSEMBLES)
    results = {}
    for held in names:
        train_ens = [e for e in names if e != held]
        predict = _train_recommender(train_ens, n_problems, rng, assessor)
        bf = _best_fixed(train_ens, p, n_train, n_test, trials, rng, assessor)
        gen, heavy = ENSEMBLES[held]
        rk_rec, rk_bf = [], []
        for _ in range(trials):
            scores, rec = _trial(
                gen, heavy, p, n_train, n_test, rng, assessor, recommender=predict
            )
            ranks = _ranks(scores)
            rk_rec.append(ranks[rec])
            rk_bf.append(ranks[bf])
        results[held] = {
            "best_fixed": bf,
            "rank_recommender": float(np.mean(rk_rec)),
            "rank_best_fixed": float(np.mean(rk_bf)),
        }
    return results


def report(results) -> str:
    header = (
        f"{'held-out ensemble':22}{'best_fixed (on rest)':>24}"
        f"{'rank_rec':>10}{'rank_fix':>10}{'win':>5}"
    )
    lines = [header, "-" * 71]
    rec_tot, fix_tot = 0.0, 0.0
    for name, r in results.items():
        win = "rec" if r["rank_recommender"] <= r["rank_best_fixed"] else "fix"
        rec_tot += r["rank_recommender"]
        fix_tot += r["rank_best_fixed"]
        lines.append(
            f"{name:22}{r['best_fixed']:>24}{r['rank_recommender']:>10.2f}"
            f"{r['rank_best_fixed']:>10.2f}{win:>5}"
        )
    n = len(results)
    lines.append("-" * 71)
    lines.append(f"{'MEAN rank (1=oracle)':22}{'':>24}{rec_tot / n:>10.2f}{fix_tot / n:>10.2f}")
    return "\n".join(lines)


if __name__ == "__main__":
    src = "randomcov + numpy" if HAVE_RANDOMCOV else "numpy ensembles"
    print(f"Out-of-sample recommender validation  [{src}; assessor = GMVVariance]\n")
    print("== shipped frozen recommender (suggest), leave-one-ensemble-out ==")
    print(report(leave_one_ensemble_out()))
    print("\n== trained recommender, leak-free leave-one-FAMILY-out ==")
    print("   (per held-out family, a fresh tree is trained on the other families only)\n")
    print(report(leave_one_family_out_trained()))
