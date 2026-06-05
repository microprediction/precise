---
name: assess-covariance-method
description: Rigorously and honestly assess a NEW or proposed covariance / correlation / precision estimator, or a new covariance scoring rule, using precise. Use when someone proposes, asks to evaluate, or wants to compare a covariance methodology. Covers implementing it to the contract, conformance, benchmarking against the registry, out-of-sample validation, and statistically defensible inference.
---

# Assess a new covariance/correlation methodology

A protocol for turning "here's a covariance idea" into a defensible verdict. Work the steps in order;
stop early only if a step fails. Install: `pip install precise[research]` (the `research/` scripts use
scikit-learn and `randomcov`).

## 0. Classify the method first

- **Estimator** (produces a matrix) vs **assessor** (scores a matrix)? Different paths below.
- **Online** (updatable per observation) or **batch**? precise is an online library; a batch method can
  still be wrapped, but say so.
- Does it target the **covariance**, **correlation**, or **precision**? It must expose, or be convertible
  to, `covariance_`.
- Does evaluating it **need the ground-truth** covariance (simulation only) or work on real data?

## 1. Implement it to the contract

Subclass `BaseOnlineCovariance`. The cheapest correct route: **copy the simplest existing estimator and
modify it** — read `precise/empirical.py` (and `precise/base.py` for the exact hook signatures, typically
`_init_state` / `_update_state` / `_state_to_cov` / `_state_to_mean`). The base class owns `partial_fit`,
`fit`, and the derived attributes; the subclass only supplies the state update and the map to a covariance.
Register it in `precise/registry.py` so `all_estimators()` includes it.

A scoring rule instead? Implement an `Assessor` (see `precise/assessment/`), set `needs_data` /
`needs_truth`, and follow the **higher = better** convention.

## 2. Conformance — non-negotiable

Run the conformance suite (`tests/test_estimators.py` parametrizes over `all_estimators()`), or check the
invariants directly:

- `covariance_` is symmetric and PSD (eigenvalues ≥ 0);
- `correlation_` has unit diagonal; `precision_ @ covariance_ ≈ I` when well-conditioned;
- streaming rows via `partial_fit` equals `fit(X)` for non-windowed estimators;
- `set_state(get_state())` round-trips;
- it runs on the numpy-only install (no hidden heavy deps).

If it fails any of these, fix the implementation before any benchmarking — numbers from a non-conformant
estimator are meaningless.

## 3. Pick the right judge BEFORE looking at results

This is where most covariance evaluations go wrong. **In high dimensions (`p` comparable to `n`), do not
rank estimators by the held-out Gaussian likelihood** — it is dominated by unidentifiable small eigenvalues
and ranks estimators below chance. Use the assessor panel and choose by regime (see the
**score-covariance-estimate** skill): `BlockPseudoLikelihood` / `SchurLikelihood` / `VariogramScore` /
`GMVVariance` in high-d; `LogLikelihood` only when low-d and well-conditioned; a QLIKE/Bregman-consistent
loss (not RMSE) when the target is a noisy variance proxy. To choose defensibly, measure the **statistical
power** of candidate judges — the probability they reproduce a known quality ordering — with
`research/metric_power.py`.

## 4. Benchmark against the registry

`research/bakeoff.py` runs every estimator over discriminating scenarios and scores them with
`all_assessors()`. Add the new estimator and compare. Report **relative error vs a naive / shrinkage
baseline within each scenario, then averaged** (RMSE is scale-sensitive and can be won by doing well only
in high-volatility regimes). Always include a `0`/historical-mean baseline for returns-like targets.

## 5. Sweep the data-generating process — results are ensemble-sensitive

A win on one generator need not transfer. Generate ground truth across several ensembles (LKJ, Wishart,
factor/spiked, Toeplitz/AR, equicorrelation) with `randomcov` plus plain numpy, sample from each, and
**report per-ensemble, not just pooled**. A single ensemble can manufacture or hide any effect.

## 6. Out-of-sample and real data; be honest about selectors

- Out-of-sample on synthetic ensembles: `research/oos.py`. On real equity data: `research/oos_equity.py`
  (bundled Ken French returns, no key needed).
- If the method is a **recommender / selector** (chooses among estimators), evaluate it
  **leave-one-generative-family-out** (`leave_one_family_out_trained` in `research/oos.py`), not
  leave-one-sample-out — selectors generalize across samples far more easily than across novel structure,
  and the difference is exactly where they fail.
- **Report nulls.** If it ties or loses, say so plainly with the number; a method that "matches the best
  fixed estimator and avoids catastrophe" is a real but smaller claim than "beats it."

## 7. Inference done right

Pairwise significance is the easiest thing to get wrong. The loss differentials are almost always
**dependent**: overlapping forecast horizons, rolling/trailing targets, repeated expanding-window splits,
cross-asset correlation, and many pairwise comparisons. Consequently:

- A naive Diebold–Mariano statistic, or standard-error bars computed as if splits were independent,
  **overstates significance**. Treat such bars as descriptive, not as confidence intervals.
- Use a **block bootstrap over dates (and clustering over correlated assets)**, or the **Model Confidence
  Set** (Hansen, Lunde & Nason 2011), which handles dependence and multiplicity together — preferable to a
  wall of pairwise stars.
- State one- vs two-sided, and any multiple-comparison treatment.
- Watch the **trailing-vs-forward target trap**: if the "target" is a rolling window that overlaps already
  observed data (e.g. next value of a 7-day trailing std), the task is partly mechanical and apparent
  forecastability is an artifact. Define targets so the forecast origin uses only past information.

## 8. Honest reporting checklist

- State exactly what was estimated and scored, and which assessor (and why, given the dimension).
- Give effect sizes and relative errors, not just p-values.
- Report per-ensemble and on real data; note where the method loses.
- Don't read point-error gains as economic/trading signals.
- Ship the code and tests so the numbers are reproducible (this repo's `research/` scripts are the model:
  each headline number has a runnable script and a guarding test).

## Reference

- Estimator contract: `precise/base.py`, `precise/empirical.py`; registry: `precise/registry.py`.
- Assessors: `precise/assessment/`; panel via `all_assessors()`.
- Experiments: `research/bakeoff.py`, `research/metric_power.py`, `research/oos.py`,
  `research/oos_equity.py`; Schur-likelihood theory: `research/schur_*.py`.
- Background on why the high-dimensional likelihood fails and what to use instead:
  <https://precise.microprediction.org/papers/schur-likelihood/>.
