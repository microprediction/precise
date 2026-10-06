# precise

[![PyPI](https://img.shields.io/pypi/v/precise)](https://pypi.org/project/precise/)
[![ci](https://github.com/microprediction/precise/actions/workflows/ci.yml/badge.svg)](https://github.com/microprediction/precise/actions/workflows/ci.yml)
[![coverage ≥95%](https://img.shields.io/badge/coverage-%E2%89%A595%25-brightgreen)](https://github.com/microprediction/precise/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/precise)](https://pypi.org/project/precise/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/microprediction/precise/blob/main/LICENSE)

<!-- The coverage badge states the floor that CI enforces (pytest --cov-fail-under=95 in ci.yml). -->

**Online (incremental) covariance and correlation estimation** — the streaming complement to
[`sklearn.covariance`](https://scikit-learn.org/stable/modules/covariance.html), whose estimators
are batch-only and have no `partial_fit`. Pure Python + numpy; no other required dependencies. And
because no estimator wins everywhere, `precise` also **assesses** an estimate and **recommends** one
for your data (see [Assess &amp; recommend](#assess--recommend)).

📖 Docs: **[precise.microprediction.org](https://precise.microprediction.org)**

```bash
pip install precise
```

## Who it is for

Researchers and engineers who need a covariance, correlation or precision matrix that is kept up
to date as data arrives, rather than recomputed from scratch: in statistics, econometrics,
empirical finance, signal processing and online machine learning. It is also a test bed for
*studying* covariance estimators: twenty estimators share one contract, so they can be compared on
the same stream, scored with the same assessors, and swapped without changing the calling code.

Research uses so far:

- the author's unrefereed working papers
  [*Schur Covariance Evaluation*](https://precise.microprediction.org/papers/schur-likelihood/)
  (scoring covariance estimates in high dimensions),
  [*Two Sides of Schur Damping*](https://precise.microprediction.org/papers/two-sides-of-schur-damping/)
  and the note [*Spectral Calibration Without a
  Split*](https://precise.microprediction.org/papers/online-spectral-calibration/), with
  reproduction scripts in [`research/`](https://github.com/microprediction/precise/tree/main/research);
- [river](https://github.com/online-ml/river), the online machine-learning library, which ported
  four of precise's estimators into `river.covariance` (see [Comparison](#comparison-with-other-packages)).

## Use

```python
import numpy as np
from precise import EwaCovariance

stream = np.random.default_rng(0).standard_normal((500, 4))   # stand-in for your data

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
| `DiagonalCovariance` | variances only (independent variables) |
| `BlockCovariance` | block-diagonal, with O(p·b) state for very large p |
| `EwaCovariance` | exponentially weighted (recency-biased) |
| `AdaptiveEwaCovariance` | EWMA whose forgetting rate speeds up on regime change |
| `LedoitWolfCovariance` | online Ledoit-Wolf shrinkage towards a scaled identity |
| `OASCovariance` | online Oracle Approximating Shrinkage (often better-conditioned than LW) |
| `ShrunkCovariance` | fixed-intensity shrinkage to identity **or** a constant-correlation target |
| `NonlinearShrinkageCovariance` | analytical *nonlinear* spectrum shrinkage — each eigenvalue moved separately, sample eigenvectors kept |
| `WindowedNonlinearShrinkageCovariance` | the same map over a rolling window — forgets, and equal weights keep the asymptotics exact |
| `EwaNonlinearShrinkageCovariance` | the same map over an exponentially weighted sample — approximate, but no window boundary to echo shocks |
| `PartialMomentsCovariance` | exponentially weighted partial-moment (semi-)covariance |
| `HuberCovariance` | online robust estimator that downweights outliers |
| `TylerCovariance` | recursive Tyler M-estimator — robust correlation/shape for elliptical data |
| `GeodesicEwaCovariance` | recency-weighted update along the affine-invariant SPD geodesic |
| `DCCCovariance` | dynamic conditional correlation — decouples volatility from correlation |
| `FactorCovariance` | online low-rank + diagonal (approximate factor model); O(d·k) per step |
| `SchurCovariance` | *experimental*: damps cross-block coupling by a fixed `gamma` |
| `SchurLedoitWolfCovariance` | *experimental*: cross-block damping set by a Ledoit-Wolf reliability estimate |
| `SchurConditionalCovariance` | *experimental*: damped, ridge-regressed block conditionals |

**Experimental** marks methods that are new with this package: they have not been peer-reviewed or
validated outside it, and their behaviour may change between minor releases. The same applies to
the `SchurLikelihood` assessor and to `suggest()` below. Everything else implements an
established method.

```python
from precise import all_estimators, estimator_from_name
all_estimators()                          # the list of classes (a bake-off in one loop)
estimator_from_name("LedoitWolfCovariance")
```

## Keyed / dynamic universes (river-style)

In streaming/finance settings observations arrive as **dicts keyed by name**, and the set of names
can change over time. `keyed(...)` decorates *any* of the estimators above to consume keyed dicts
(river-style `update` / `learn_one`) and emit keyed output:

```python
from precise import keyed, EwaCovariance

d = keyed(EwaCovariance(r=0.05), dynamic=True)   # changing universe (DynamicUniverse)
d.update({"AAPL": 0.01, "MSFT": -0.02})
d.update({"MSFT": 0.00, "NVDA": 0.03})           # AAPL leaves, NVDA enters
d.covariance_                                     # dict-of-dicts over the live universe
d.to_frame()                                      # pandas DataFrame  (pip install precise[pandas])

k = keyed(EwaCovariance(r=0.05))                  # fixed universe, imputes missing keys (FixedUniverse)
```

`dynamic=False` (the default) gives a `FixedUniverse` (one wrapped estimator, missing keys imputed);
`dynamic=True` gives a `DynamicUniverse` (a wrapped estimator per live key-set). Both work with any
positional estimator — the adapter adds no covariance math of its own.

## Composing volatility × correlation

`H = D R D` is a composition, not a fixed algorithm. `ConditionalCovariance` lets you pick the
per-series **volatility** model and the **correlation** estimator independently — `DCCCovariance` is
just the EWMA/EWMA special case:

```python
from precise import ConditionalCovariance, EwaCovariance, LedoitWolfCovariance

est = ConditionalCovariance(vol=EwaCovariance(r=0.02),       # any estimator, used per series in 1-D
                            corr=LedoitWolfCovariance(r=0.05))  # correlation from any estimator
```

The volatility model can also be any univariate model from
[microprediction/skaters](https://github.com/microprediction/skaters) (Holt, Hosking, …) via
`from_skater` — precise doesn't depend on it; the adapter is duck-typed:

```python
import skaters
from precise import ConditionalCovariance, from_skater
est = ConditionalCovariance(vol=from_skater(skaters.holt), corr=EwaCovariance(r=0.05))
```

## Assess & recommend

No estimator wins everywhere, so `precise` treats *judging* and *choosing* an estimate as
first-class alongside producing one.

```python
from precise import all_assessors, suggest

all_assessors()             # scoring rules: LogLikelihood, BlockPseudoLikelihood, SchurLikelihood,
                            # SteinLoss, FrobeniusToTruth, GMVVariance, ... (higher = better)
suggest(X, top=3)           # recommend estimator classes from observable features of X
```

`suggest` (*experimental*) maps truth-free features of your data (p/n, effective rank, sphericity,
condition number, off-diagonal mass, excess kurtosis) to an estimator, via a frozen, numpy-only
decision tree trained on simulated data. Its own benchmarks find that choosing per data set is
close to, and sometimes worse than, always using one good estimator, except when the number of
variables approaches the number of observations, so treat its answer as a starting point. The
**Schur pseudo-likelihood** (*experimental*), a one-parameter (`γ`) bridge between the full and
block-diagonal Gaussian likelihoods, is both an assessor here and the subject of an unrefereed
[working paper](https://github.com/microprediction/precise/blob/main/papers/schur_likelihood_paper.pdf).

## Comparison with other packages

- **[`sklearn.covariance`](https://scikit-learn.org/stable/modules/covariance.html)** is the
  reference batch implementation (empirical, Ledoit-Wolf, OAS, shrunk, minimum covariance
  determinant, graphical lasso). None of its estimators has `partial_fit`: each needs the whole
  sample at once. precise follows its naming and attribute conventions (`covariance_`,
  `precision_`, `location_`), so moving between the two is easy.
- **[`river.covariance`](https://riverml.xyz/)** is the closest relative. River is a general
  online machine-learning library, and its covariance module had `EmpiricalCovariance` and
  `EmpiricalPrecision`. In July 2026 river
  [PR #1923](https://github.com/online-ml/river/pull/1923) ported precise's `EwaCovariance`,
  `LedoitWolfCovariance`, `OASCovariance` and `ShrunkCovariance` into `river.covariance`, crediting
  precise, and added `EwaPrecision`, which tracks the inverse directly by Sherman-Morrison updates
  (precise computes `precision_` by inverting on read). They shipped in river 0.26.0. If you
  already use river and need one of those, use river's: its estimators are dict-native, take
  mini-batches from any narwhals dataframe, and fit river pipelines. River chose to take only estimators that never
  invert a stored matrix on read, so what precise still offers beyond it is:
  - estimators river does not have: nonlinear spectral shrinkage (expanding, rolling-window and
    exponentially weighted), robust M-estimators (Huber, Tyler), DCC and composed
    volatility × correlation models, an online factor model, partial-moment (semi-)covariance,
    adaptive forgetting, geodesic updates, block-diagonal estimators and the experimental Schur
    family;
  - one numpy contract shared by all twenty, with a registry, so a bake-off is one loop;
  - mid-stream checkpointing: every estimator's state is a plain, JSON-friendly dict;
  - assessors for scoring an estimate out of sample, and a recommender;
  - keyed adapters that turn *any* of the estimators into a dict-keyed one over a universe whose
    names enter and leave.
- **[skfolio](https://skfolio.org)** and **PyPortfolioOpt** include covariance estimators as part of
  portfolio optimization, in batch form.

## Development install

```bash
git clone https://github.com/microprediction/precise.git
cd precise
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                               # run the test suite
ruff check precise tests research    # lint
mypy precise                         # type check
```

See [CONTRIBUTING.md](https://github.com/microprediction/precise/blob/main/CONTRIBUTING.md) for the full
workflow.

## Contributing and support

Questions, bug reports and pull requests are welcome on
[GitHub issues](https://github.com/microprediction/precise/issues). The maintainer answers on a
best-effort basis, and reports of silently wrong results come first. See
[CONTRIBUTING.md](https://github.com/microprediction/precise/blob/main/CONTRIBUTING.md) for how to report a problem or propose a change, and the
[Code of Conduct](https://github.com/microprediction/precise/blob/main/CODE_OF_CONDUCT.md).

Much of the 1.x code was written with AI coding assistants under the author's direction;
[AI_USE.md](https://github.com/microprediction/precise/blob/main/AI_USE.md) says how, and how the code is checked.

## Citing

If you use precise in your research, please cite it. [CITATION.cff](https://github.com/microprediction/precise/blob/main/CITATION.cff) holds the
metadata, and GitHub's "Cite this repository" button formats it. For example:

> Cotton, P. (2026). *precise: online covariance, correlation and precision matrix estimation in
> Python* (version 1.1.0) [Computer software]. https://github.com/microprediction/precise

## Related

- **Generating** random covariance/correlation matrices to test against: [`randomcov`](https://github.com/microprediction/randomcov).
- **Portfolio construction** (Schur-complementary allocation, HRP) is no longer part of precise:
  it moved out at 1.0 to [allocation.microprediction.org](https://allocation.microprediction.org),
  and for production use the [skfolio](https://skfolio.org/auto_examples/clustering/plot_6_schur.html)
  implementation is recommended. precise estimates covariance; it does not build portfolios.
- A [Robust Portfolio Literature Reading List](https://github.com/microprediction/precise/blob/main/LITERATURE.md) lives in this repo.
- Part of the [microprediction](https://github.com/microprediction/microprediction) project.

> Migrating from precise &lt; 1.0 (the functional "skater" API)? See [MIGRATING.md](https://github.com/microprediction/precise/blob/main/MIGRATING.md).

## Disclaimer

Not investment advice. Just code, subject to the MIT License.
