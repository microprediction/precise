# Migrating to precise 1.0

precise 1.0 is a focused rewrite: it does **online covariance and correlation estimation**, and
nothing else. The API moved from the old functional "skater" convention to sklearn-style
estimator classes, and portfolio construction moved out of the package entirely.

## Covariance estimation

**Before (precise < 1.0)** — functional skaters threading a state dict:

```python
from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r005_n100 as f
s = {}
for y in ys:
    x, x_cov, s = f(s=s, y=y)
```

**Now** — sklearn-style estimator classes with `partial_fit`:

```python
from precise import PartialMomentsCovariance
est = PartialMomentsCovariance(r=0.05)
for y in ys:
    est.partial_fit(y)
x_cov = est.covariance_          # also .correlation_, .precision_, .location_
```

The hundreds of frozen, parameter-baked skater names (`*_r005_n100`, `d0`/`d1`, …) are replaced by
a handful of parameterized classes:

| Old family (module) | New class |
|---|---|
| `runemp`, `bufemp` | `EmpiricalCovariance` |
| `ewaemp` | `EwaCovariance` |
| `ewalw`, `ewalz`, `weaklz` | `LedoitWolfCovariance` |
| `ewapm`, `weakpm` | `PartialMomentsCovariance` |
| `bufhuber` | `HuberCovariance` |
| *(new)* | `GeodesicEwaCovariance` |

The `d0`/`d1` distinction (levels vs first differences) is now the `diff=` flag, e.g.
`EwaCovariance(r=0.05, diff=True)`. Use `precise.all_estimators()` to enumerate every estimator.

## Dynamic universes

The dict-keyed `SkaterCovariance` (variables entering/leaving) is replaced by the `keyed(...)`
adapters, which decorate any positional estimator with a river-style `update` / `learn_one` surface:

```python
from precise import keyed, EwaCovariance
d = keyed(EwaCovariance(r=0.05), dynamic=True)   # DynamicUniverse: names enter/leave
d.update({"AAPL": 0.01, "MSFT": -0.02})
d.covariance_   # dict-of-dicts;  d.to_frame() for a pandas DataFrame

k = keyed(EwaCovariance(r=0.05))                 # FixedUniverse: fixed names, missing keys imputed
```

## Portfolio construction, managers, and the Schur work

All allocation/portfolio/manager code (`portfoliostatic`, `portfolioutil`, `managers`,
`managerutil`, Schur-complementary allocation) has been **removed** from precise. It now lives at
[microprediction/allocation](https://github.com/microprediction/allocation) (allocation.microprediction.org); for production use the
[skfolio](https://skfolio.org/auto_examples/clustering/plot_6_schur.html) implementation is
recommended. The pre-1.0 source remains in this repository's git history (see commit `3670edd`,
the last commit before the 1.0 rewrite) if you need to reference the original implementations.

## Benchmarking / elo bake-offs

The elo bake-off apparatus moved to the non-shipped `research/` directory (`legacy_skatervaluation`),
preserved pending a rewrite against the new `all_estimators()` contract. It is not part of the
installed package.
