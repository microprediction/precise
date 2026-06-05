---
name: choose-covariance-estimator
description: Pick which precise covariance estimator to use for a given dataset. Use when you have data X and are unsure which estimator fits its dimension, conditioning, or tail behavior. Wraps precise.suggest() and covariance_features().
---

# Choose a covariance estimator for your data

No estimator wins everywhere, so `precise` recommends one from observable, truth-free features.

```python
from precise import suggest, covariance_features

suggest(X, top=3)        # -> list of estimator CLASSES, best first
covariance_features(X)   # -> dict of the features behind the choice
```

`X` is 2-D (rows = observations, columns = variables). Then:

```python
Est = suggest(X, top=1)[0]
est = Est()
est.fit(X)               # or stream rows with partial_fit
cov = est.covariance_
```

## What it keys on

`covariance_features(X)` returns `p`, `n`, `p_over_n`, `effective_rank`, `sphericity`,
`condition_number`, `mean_abs_offdiag_corr`, `avg_excess_kurtosis` — all computed from the sample, none
requiring the unknown truth. Internally `suggest` uses a frozen, numpy-only decision tree; broadly it
routes high `p/n` or ill-conditioned data to shrinkage/factor estimators and heavy-tailed data to robust
ones.

## Guardrail (important)

`suggest` is a heuristic trained on synthetic regimes. In leave-one-generative-family-out tests it does
**not** reliably beat the single best fixed estimator on a *wholly novel* data-generating family — it
generalizes across samples within familiar regimes, not to arbitrarily new structure. So:

- Treat its output as a strong shortlist, not an oracle.
- If the decision matters, **verify** the shortlist out-of-sample on your own data with the
  **score-covariance-estimate** skill, rather than trusting the recommendation blind.
- A well-conditioned shrinkage estimator (`LedoitWolfCovariance` / `OASCovariance`) is a safe default
  when in doubt.
