"""Real-data out-of-sample validation of the recommender, on Ken French industry returns.

The decisive half of the recommendation proof: on *real* equity returns, does choosing the
covariance estimator per-window from observable features (``precise.suggest``) beat the best single
fixed estimator out of sample? We use the canonical economic criterion — the realized out-of-sample
variance of the global-minimum-variance portfolio ``w ∝ Σ̂⁻¹1`` (Ledoit-Wolf; Engle-Ledoit-Wolf;
de Prado) — over rolling windows. No true covariance is needed; realized risk is the judge.

Data: Ken French 49 Industry Portfolios, daily (``research/data/ff49_industry_daily.csv``). At a
~60-day training window with p=49 this is the high-dimensional regime (p/n ≈ 0.8) where estimator
choice matters most.

    pip install precise[research]   # needs pandas
    python research/oos_equity.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from precise import all_estimators, suggest
from precise._linalg import try_invert

DATA = Path(__file__).parent / "data" / "ff49_industry_daily.csv"


def _load_returns(path=DATA):
    import pandas as pd

    df = pd.read_csv(path, index_col=0)
    return df.values, list(df.columns)


def _gmv_weights(cov):
    w = try_invert(cov) @ np.ones(len(cov))
    return w / w.sum()


def rolling_oos(returns, train_len=60, test_len=21, step=21):
    """Rolling min-variance OOS realized variance for every estimator + the recommender.

    Returns ``(fixed, recommender, oracle, equal_weight, recommend_counts)`` as annualized vols.
    """
    R = np.asarray(returns, dtype=float)
    T, p = R.shape
    ests = all_estimators()
    per_roll = {E.__name__: [] for E in ests}
    rec_roll, ew_roll, oracle_roll = [], [], []
    counts: dict = {}

    for t in range(0, T - train_len - test_len + 1, step):
        train = R[t : t + train_len]
        test = R[t + train_len : t + train_len + test_len]
        this = {}
        for E in ests:
            w = _gmv_weights(E().fit(train).covariance_)
            this[E.__name__] = float(np.mean((test @ w) ** 2))
            per_roll[E.__name__].append(this[E.__name__])
        rec = suggest(train, top=1)[0].__name__
        counts[rec] = counts.get(rec, 0) + 1
        rec_roll.append(this[rec])
        oracle_roll.append(min(this.values()))
        ew = np.ones(p) / p
        ew_roll.append(float(np.mean((test @ ew) ** 2)))

    def annvol(v):
        return float(np.sqrt(252.0 * np.mean(v)))

    fixed = {k: annvol(v) for k, v in per_roll.items()}
    return fixed, annvol(rec_roll), annvol(oracle_roll), annvol(ew_roll), counts


def report(fixed, recommender, oracle, equal_weight, counts) -> str:
    ranked = sorted(fixed.items(), key=lambda kv: kv[1])
    best_fixed_name, best_fixed_vol = ranked[0]
    rec_rank = 1 + sum(v < recommender for v in fixed.values())
    lines = [
        "Real-data OOS: annualized min-variance volatility (lower is better)",
        f"{'estimator (fixed)':26}{'ann_vol':>10}",
        "-" * 36,
    ]
    for name, v in ranked:
        lines.append(f"{name:26}{v:>10.4f}")
    lines += [
        "-" * 36,
        f"{'equal_weight':26}{equal_weight:>10.4f}",
        f"{'ORACLE (per-window best)':26}{oracle:>10.4f}",
        f"{'RECOMMENDER (suggest)':26}{recommender:>10.4f}   rank {rec_rank}/{len(fixed)}",
        f"{'best single fixed':26}{best_fixed_vol:>10.4f}   ({best_fixed_name})",
        "",
        f"recommender picks: {counts}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    returns, _ = _load_returns()
    print(f"Ken French 49 Industry daily returns: {returns.shape}\n")
    print(report(*rolling_oos(returns)))
