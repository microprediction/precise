# Changelog

All notable changes to `precise` are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project aims to follow
[Semantic Versioning](https://semver.org/).

## [1.0.0] — unreleased

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
  [`schur`](https://github.com/microprediction/schur).

See `MIGRATING.md` for the upgrade path.

## [1.0.0rc1] — 2026-06-05

First pre-release of the 1.0 line (for testing the makeover; `pip install precise` continues to serve
the 0.16.x line until 1.0.0 final).

## [0.16.7] and earlier

The original `precise` (functional skater API, portfolio construction, elo benchmarking). See the
git history.

[1.0.0]: https://github.com/microprediction/precise/releases
[1.0.0rc1]: https://github.com/microprediction/precise/releases/tag/v1.0.0rc1
