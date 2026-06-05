---
name: keyed-dynamic-universe
description: Maintain an online covariance over named series whose set changes over time (e.g. assets entering and leaving). Use when observations arrive as dicts keyed by name rather than fixed-length vectors. Wraps precise's keyed / FixedUniverse / DynamicUniverse adapters.
---

# Keyed covariance over a changing universe

In streaming/finance settings observations are dicts keyed by name, and the set of names changes. `keyed`
decorates *any* positional estimator to consume keyed dicts and emit keyed output.

```bash
pip install precise            # add [pandas] for to_frame()
```

```python
from precise import keyed, EwaCovariance

est = keyed(EwaCovariance(r=0.05), dynamic=True)     # universe may change over time
est.partial_fit({"BTC": 0.01, "ETH": -0.02})         # river-style: also .update / .learn_one
est.partial_fit({"ETH": 0.00, "SOL": 0.03})          # BTC drops out, SOL enters

est.covariance_["ETH"]["SOL"]                         # dict-of-dicts over the live universe
est.to_frame()                                        # pandas DataFrame  (needs [pandas])
```

## Fixed vs dynamic

- `keyed(est)` / `dynamic=False` → **FixedUniverse**: one wrapped estimator; missing keys are imputed.
  Use when the set of names is stable and you just want dict ergonomics.
- `keyed(est, dynamic=True)` → **DynamicUniverse**: tracks multiple live key-sets with staleness /
  longevity eviction and assembles a pairwise matrix. Use when names genuinely enter and leave.

## Notes

- The adapter adds **no covariance math of its own** — it wraps the positional estimator, so any estimator
  from the **estimate-online-covariance** skill works inside it (`LedoitWolfCovariance`, `HuberCovariance`,
  …).
- The assembled matrix is projected to the nearest PSD; expect small adjustments when the live universe
  changes.
- To score/compare keyed estimators, extract the dense `covariance_` (e.g. via `to_frame().values`) and use
  the **score-covariance-estimate** skill.
