---
name: estimate-online-covariance
description: Estimate a covariance / correlation / precision matrix incrementally with precise. Use when data arrives as a stream and you want the matrix updated per observation, or when you want an online (partial_fit) drop-in for sklearn.covariance, which is batch-only.
---

# Estimate online covariance with precise

`precise` provides sklearn-style estimators with a single `partial_fit` contract. Pure numpy.

```bash
pip install precise
```

## The pattern

```python
import numpy as np
from precise import EwaCovariance        # exponentially weighted; recency-biased

est = EwaCovariance(r=0.05)              # r in (0,1]; larger = faster forgetting
for y in stream:                         # y is a 1-D array (one observation)
    est.partial_fit(y)

est.covariance_     # (d, d) ndarray, symmetric and PSD by construction
est.correlation_    # unit-diagonal correlation
est.precision_      # inverse covariance (when well-conditioned)
est.location_       # running mean
est.n_samples_      # observations seen
```

`fit(X)` is the batch drop-in (`X` is 2-D, rows = observations); it resets then replays rows, so
it matches `sklearn.covariance`'s call shape.

## Choosing the class

`all_estimators()` lists every estimator; `estimator_from_name("LedoitWolfCovariance")` looks one up.
Sensible defaults by situation:

- general / recency-weighted: `EwaCovariance(r=...)`
- many variables relative to samples (p/n large) or ill-conditioned: `LedoitWolfCovariance`, `OASCovariance`, `ShrunkCovariance`, `FactorCovariance`
- heavy tails / outliers: `HuberCovariance`, `TylerCovariance`
- regime changes: `AdaptiveEwaCovariance`, `DCCCovariance`
- you don't know: use the **choose-covariance-estimator** skill (`suggest(X)`).

## Notes

- All estimators are truly online — constant work per observation, no growing buffers.
- State is a JSON-able dict: `est.get_state()` / `est.set_state(s)` for mid-stream checkpointing.
- `covariance_` is always symmetric PSD; don't hand-symmetrize or clip it yourself.
- Named series with a changing universe? Use the **keyed-dynamic-universe** skill instead.
