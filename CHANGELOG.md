# Changelog

All notable changes to `precise` are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project aims to follow
[Semantic Versioning](https://semver.org/).

## [1.1.0] — 2026-09-13

### Added
- `NonlinearShrinkageCovariance`: online analytical **nonlinear** shrinkage of the covariance
  spectrum (Ledoit & Wolf 2020). The zoo's linear shrinkers pull every eigenvalue towards a common
  target; this moves each one separately while keeping the sample eigenvectors, and stays finite and
  invertible when `p > n`. Accumulation is a plain Welford update (O(p^2)/step, no window); the
  spectral work is lazy, in `_state_to_cov`, and memoized per state.
- `WindowedNonlinearShrinkageCovariance`: the same map over a rolling window of the last `W`
  observations. A window is the forgetting variant that keeps the asymptotics *exact* — equal
  weights inside the window are precisely the sample they describe, with `n = W` — where an
  exponential decay would need the weighted theory rather than a moment-matched effective sample
  size. Bounded state, O(p^2) add-and-drop per step. `research/forgetting.py` scores the two
  against each other; `research/turnover.py` scores what squared error cannot see — the window's
  hard boundary echoes every shock one window later, which costs churn that grows with tail
  weight.
- `EwaNonlinearShrinkageCovariance`: the same map over an exponentially weighted sample, at
  `n_eff = (2-r)/r`. Statistically the approximate one — matching one moment of the weight
  distribution is not an equivalence, and Oriol (arXiv:2410.14420) derives the weighted formulas
  properly — but it has no window boundary, so it does not pay for a shock twice.
  `research/turnover.py` measures the difference.
- A JOSS paper under `papers/joss/`, and the note *Spectral Calibration Without a Split* under
  `papers/online_spectral_calibration/`.

### Fixed
- `LedoitWolfCovariance` collapsed to a scaled identity under heavy tails. `pi_bar` averages a
  quantity growing like the fourth power of the observation, so one fat-tailed draw could pin the
  shrinkage intensity at 1 and leave the estimate with no off-diagonals: at t(3) innovations it
  retained 0.088 of the covariance structure where OAS retained 0.543. Each observation's
  contribution is now winsorized at ten times the running mean, which leaves Gaussian behaviour
  unchanged to three decimals and takes t(3) retention to 0.409.
- The frozen recommender was inert. `sklearn`'s `tree_.value` holds class proportions, and the
  exporter cast them with `int()`, flooring every value under 1.0 to zero — 46 of 47 nodes carried
  no weight, so `suggest()` had been ranking on the heuristic ruleset alone. The model now covers
  19 of 20 estimators (it was 9), and two training runs produce a byte-identical artifact.
- Training was irreproducible whenever `randomcov` was installed: three generative ensembles in
  `research/oos.py` ignored the `rng` they were passed and drew from global state.
- The training grid stopped at `n/p = 3`, so every data-rich low-dimensional problem was
  extrapolation. It now spans `p` from 5 to 60 and `n/p` from 0.5 to 25.
- A malformed generated model can no longer break `import precise`.

### Changed
- `suggest()`'s safe default moves from `LedoitWolfCovariance` to `NonlinearShrinkageCovariance`,
  which has the best mean rank of any single fixed choice over eleven ensembles and seven `(p, n)`
  regimes. It is not uniformly best: at `p` close to `n` it ranks 9.41 and the trained model is
  worth far more there, which is why the model still leads and this only breaks ties.

## [1.0.0] — 2026-06-05

A ground-up rewrite: `precise` is now a focused library for **online (incremental) covariance and
correlation estimation** — the online complement to `sklearn.covariance`.

### Added
- sklearn-style online estimator classes with a single `partial_fit` contract and
  `covariance_` / `correlation_` / `precision_` / `location_` attributes; 14 estimators via
  `all_estimators()` (Empirical, Diagonal, Ewa, AdaptiveEwa, LedoitWolf, OAS, Shrunk, Schur,
  PartialMoments, Huber, Tyler, GeodesicEwa, DCC, Factor).
- Keyed, river-style adapters (`keyed`, `FixedUniverse`, `DynamicUniverse`) for dynamic universes of
  named variables that enter and leave.
- An assessment layer (`all_assessors()`), including the Schur (pseudo-)likelihood judge.
- A recommender (`suggest`, `covariance_features`) — a frozen, numpy-only decision tree.
- `py.typed` marker: the package now ships its type information.
- Packaging via `pyproject.toml` / hatchling; `numpy`-only core with optional `[pandas]`,
  `[research]`, `[dev]`, `[docs]` extras.

### Changed
- numpy is the only required dependency (`numpy>=1.21`); verified on numpy 1.26 and 2.x.

### Removed
- **Breaking:** the functional "skater" API (`precise.skaters.*`) is removed — importing it now
  raises a pointer to `MIGRATING.md`.
- **Breaking:** portfolio / manager / Schur **allocation** code moved to
  [`allocation`](https://github.com/microprediction/allocation).

See `MIGRATING.md` for the upgrade path.

## [1.0.0rc1] — 2026-06-05

First pre-release of the 1.0 line (for testing the makeover; `pip install precise` continues to serve
the 0.16.x line until 1.0.0 final).

## [0.16.7] and earlier

The original `precise` (functional skater API, portfolio construction, elo benchmarking). See the
git history.

[1.0.0]: https://github.com/microprediction/precise/releases
[1.0.0rc1]: https://github.com/microprediction/precise/releases/tag/v1.0.0rc1
