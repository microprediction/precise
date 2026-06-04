# precise

![ci](https://github.com/microprediction/precise/workflows/ci/badge.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)

**Online (incremental) covariance and correlation estimation** — the streaming complement to
[`sklearn.covariance`](https://scikit-learn.org/stable/modules/covariance.html), whose estimators
are batch-only and have no `partial_fit`. Pure Python + numpy; no other required dependencies.

```bash
pip install precise
```

## Use

```python
from precise import EwaCovariance

est = EwaCovariance(r=0.05)
for y in stream:            # y is a 1d observation; pass a 2d array for a batch
    est.partial_fit(y)

est.covariance_             # (n, n) ndarray
est.correlation_            # unit-diagonal correlation
est.precision_             # inverse covariance
est.location_              # running mean
est.fit(X)                 # sklearn-style batch drop-in (X is 2d)
```

Every estimator is **truly online** — a constant amount of work per observation, no growing
buffers. State is a plain dict, so you can checkpoint mid-stream with `get_state()` / `set_state()`.

## Estimators

| Class | What it does |
|---|---|
| `EmpiricalCovariance` | running sample covariance (Welford) |
| `EwaCovariance` | exponentially weighted (recency-biased) |
| `LedoitWolfCovariance` | online Ledoit-Wolf shrinkage towards a scaled identity |
| `PartialMomentsCovariance` | exponentially weighted partial-moment (semi-)covariance |
| `HuberCovariance` | online robust estimator that downweights outliers |
| `GeodesicEwaCovariance` | recency-weighted update along the affine-invariant SPD geodesic |

```python
from precise import all_estimators, estimator_from_name
all_estimators()                          # the list of classes (a bake-off in one loop)
estimator_from_name("LedoitWolfCovariance")
```

## Dynamic universes (keyed, river-style)

In finance the set of variables changes over time — names enter and leave. `DynamicCovariance`
takes observations as **dicts keyed by name** and tracks a covariance whose dimension follows the
live universe (river-style `update` / `learn_one`):

```python
from precise import DynamicCovariance

d = DynamicCovariance(EwaCovariance, r=0.05)
d.update({"AAPL": 0.01, "MSFT": -0.02})
d.update({"MSFT": 0.00, "NVDA": 0.03})    # AAPL leaves, NVDA enters
d.covariance_                              # dict-of-dicts over the live universe
d.to_frame()                               # pandas DataFrame  (pip install precise[pandas])
```

## Related

- **Generating** random covariance/correlation matrices to test against: [`randomcov`](https://github.com/microprediction/randomcov).
- **Portfolio construction** (Schur-complementary allocation, HRP) moved to [`schur`](https://github.com/microprediction/schur); for production use the [skfolio](https://skfolio.org/auto_examples/clustering/plot_6_schur.html) implementation is recommended.
- A [Robust Portfolio Literature Reading List](https://github.com/microprediction/precise/blob/main/LITERATURE.md) lives in this repo.
- Part of the [microprediction](https://github.com/microprediction/microprediction) project.

> Migrating from precise &lt; 1.0 (the functional "skater" API)? See [MIGRATING.md](https://github.com/microprediction/precise/blob/main/MIGRATING.md).

## Disclaimer

Not investment advice. Just code, subject to the MIT License.
