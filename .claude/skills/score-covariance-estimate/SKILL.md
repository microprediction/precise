---
name: score-covariance-estimate
description: Score and compare covariance estimates with precise's assessor panel. Use when you need to judge an estimate out-of-sample or rank competing estimators — and especially in high dimensions, where the plain held-out likelihood is misleading.
---

# Score / rank covariance estimates

```python
from precise import all_assessors, assessor_from_name

for A in all_assessors():
    s = A().score(cov, X_test=X_test, true_cov=Sigma_true)   # higher = better
```

- `cov` is the estimate to judge; `X_test` is held-out data (rows = observations); `true_cov` is the
  population covariance (only available in simulation).
- Each assessor exposes `needs_data` and `needs_truth`; pass what it needs. Truth-free assessors work on
  real data, truth-requiring ones (e.g. `FrobeniusToTruth`) only in simulation.
- All assessors follow **higher = better**, so you can rank or argmax directly.

## The one rule that matters in high dimensions

**Do not rank estimators by the held-out Gaussian log-likelihood when `p` is comparable to `n`.** The
likelihood is dominated by the smallest, unidentifiable eigenvalues of the estimate; empirically it ranks
estimators *below chance* in that regime. Instead use inversion-free or block judges:

| Regime / goal | Use |
|---|---|
| low dimension, well-conditioned | `LogLikelihood` (it is optimal here) |
| high dimension (`p/n` near 1 or larger) | `BlockPseudoLikelihood`, `SchurLikelihood`, `VariogramScore`, `FrobeniusToTruth` (sim only) |
| economic / portfolio relevance | `GMVVariance` (out-of-sample minimum-variance variance) |
| forecasting a **variance** from a noisy proxy | a QLIKE / Bregman-consistent loss, **not** RMSE on the proxy — RMSE on a noisy variance proxy can rank inconsistently |

`SchurLikelihood(gamma=...)` is a tunable bridge: `gamma=1` is the full likelihood (fragile in high-d),
`gamma=0` the robust block-diagonal one, interior values better-conditioned than either.

## Don't over-read the numbers

- Rankings are **ensemble-sensitive**: a result on one data-generating process need not transfer. If the
  conclusion matters, sweep several generators and report per-regime (see the
  **assess-covariance-method** skill).
- A lower point error (RMSE) is not a tradable or actionable signal by itself.
- If you attach significance to a ranking, the loss differentials are usually dependent (overlapping
  windows, correlated assets); naive standard errors overstate significance — see the inference section of
  the **assess-covariance-method** skill.
