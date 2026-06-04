# precise documentation

**Online (incremental) covariance and correlation estimation** — the streaming complement to
`sklearn.covariance`.

- [Covariance estimation](https://microprediction.github.io/precise/covariance) — the estimator
  classes, `partial_fit`, and the keyed (river-style) adapters for dynamic universes.
- [Correlation estimation](https://microprediction.github.io/precise/correlation) — correlation as
  a first-class output, including dynamic conditional correlation.

```python
from precise import EwaCovariance
est = EwaCovariance(r=0.05)
for y in stream:
    est.partial_fit(y)
est.covariance_   # also .correlation_, .precision_, .location_
```

### Of note
- Generating random covariance/correlation matrices to test against: [randomcov](https://github.com/microprediction/randomcov).
- Portfolio construction (Schur-complementary allocation, HRP) lives in [schur](https://github.com/microprediction/schur); for production the [skfolio](https://skfolio.org/auto_examples/clustering/plot_6_schur.html) implementation is recommended.
- Related [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md).
- Migrating from precise &lt; 1.0? See [MIGRATING.md](https://github.com/microprediction/precise/blob/main/MIGRATING.md).
- Part of the [microprediction](https://github.com/microprediction/microprediction) project. It would be lovely if you [cite](https://github.com/microprediction/microprediction/blob/master/CITE.md).

View as [source](https://github.com/microprediction/precise/blob/main/docs/README.md) or [web](https://microprediction.github.io/precise/).
