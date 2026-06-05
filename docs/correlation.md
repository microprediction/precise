# Online correlation estimation

Correlation is a first-class output of every estimator: `correlation_` returns the covariance
normalized to unit diagonal. So any estimator on the [covariance page](https://microprediction.github.io/precise/covariance)
is also an online correlation tracker.

```python
from precise import EwaCovariance

est = EwaCovariance(r=0.05)
for y in stream:
    est.partial_fit(y)

est.correlation_   # (n, n), ones on the diagonal
```

## Dynamic conditional correlation

When you specifically want correlation dynamics that are *decoupled* from volatility — i.e. the
correlation should adapt even while individual variances drift — use `DCCCovariance`. It tracks a
per-series exponentially weighted variance and an exponentially weighted correlation of the
*standardized* residuals, on (optionally) separate timescales:

```python
from precise import DCCCovariance

est = DCCCovariance(r=0.05, vol_r=0.02)   # faster correlation, slower volatility
for y in stream:
    est.partial_fit(y)

est.correlation_   # conditional correlation
est.covariance_    # = D R D, recombined with the per-series volatilities
```

## Keyed correlation

The keyed adapters expose correlation too, as a dict-of-dicts over the live universe:

```python
from precise import keyed, EwaCovariance

d = keyed(EwaCovariance(r=0.05), dynamic=True)
d.learn_one({"AAPL": 0.01, "MSFT": -0.02})
d.correlation_     # {name: {name: corr}}
```

-+-

Documentation [home](https://microprediction.github.io/precise).
