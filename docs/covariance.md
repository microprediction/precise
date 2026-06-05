# Online covariance estimation

Every estimator is an sklearn-style class: feed it one observation at a time with `partial_fit`
(or a 2d batch), then read the fitted attributes. Updates are **truly online** — constant work per
observation, no stored window.

```python
from precise import EwaCovariance

est = EwaCovariance(r=0.05)
for y in stream:            # y is a 1d observation; a 2d array is a batch
    est.partial_fit(y)

est.covariance_             # (n, n) ndarray
est.correlation_            # unit-diagonal correlation
est.precision_              # inverse covariance
est.location_               # running mean
est.n_samples_

est.fit(X)                  # reset + fit a 2d batch (sklearn drop-in)
est.score(X_test)           # mean Gaussian log-likelihood
est.mahalanobis(X_test)     # per-row squared Mahalanobis distance
```

State is a plain dict, so you can checkpoint mid-stream with `get_state()` / `set_state()`.

## The estimators

| Class | What it does |
|---|---|
| `EmpiricalCovariance` | running sample covariance (Welford) |
| `EwaCovariance` | exponentially weighted (recency-biased) |
| `LedoitWolfCovariance` | online Ledoit-Wolf shrinkage towards a scaled identity |
| `OASCovariance` | online Oracle Approximating Shrinkage |
| `PartialMomentsCovariance` | exponentially weighted partial-moment (semi-)covariance |
| `HuberCovariance` | robust — downweights outliers by Mahalanobis distance |
| `GeodesicEwaCovariance` | recency-weighted step along the affine-invariant SPD geodesic |
| `DCCCovariance` | dynamic conditional correlation — decouples volatility from correlation |
| `FactorCovariance` | online low-rank + diagonal (approximate factor model); O(d·k) per step |

Common parameters: `r` (decay rate for the recency-weighted estimators), `diff=True` (estimate the
covariance of first differences, for integrated/level data). Enumerate them with the registry:

```python
from precise import all_estimators, estimator_from_name
all_estimators()                          # the list of classes — a bake-off in one loop
estimator_from_name("LedoitWolfCovariance")
```

## Keyed / dynamic universes (river-style)

When observations arrive as **dicts keyed by name** and the set of names changes over time, wrap any
estimator with `keyed(...)`:

```python
from precise import keyed, EwaCovariance

d = keyed(EwaCovariance(r=0.05), dynamic=True)   # DynamicUniverse: names enter/leave
d.learn_one({"AAPL": 0.01, "MSFT": -0.02})
d.covariance_                                     # dict-of-dicts;  d.to_frame() for a DataFrame

k = keyed(EwaCovariance(r=0.05))                  # FixedUniverse: fixed names, missing keys imputed
```

See also: [correlation estimation](https://microprediction.github.io/precise/correlation).

-+-

Documentation [home](https://microprediction.github.io/precise).
