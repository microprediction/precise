# research

Not shipped with the package (excluded from the wheel/sdist and from the test suite). This is the
home of the benchmarking / elo bake-offs that compare covariance estimators against ground truth.

## `bakeoff.py`

The bake-off: builds discriminating ground-truth scenarios (stationary structures, high-dim/low-n,
regime change, gross-outlier contamination, heavy tails), samples from each, streams the samples
through every estimator in `precise.all_estimators()`, and scores recovery — ranking by the
scale-invariant correlation error and printing a leaderboard plus the winner of each scenario.

```bash
python research/bakeoff.py
```

Runs out of the box on a numpy ground-truth generator. With the sibling
[`randomcov`](https://github.com/microprediction/randomcov) package installed it adds richer
generated structures (LKJ, Wishart, residuals):

```bash
pip install -e ".[research]"
```

## `legacy_skatervaluation/`

The original elo bake-off harness, **targeting the pre-1.0 functional "skater" API** (and importing
the now-removed `precise.skaters` / `precise.skatertools` modules). Preserved for reference; it does
not run against precise 1.0 and is pending a rewrite to the `all_estimators()` / `partial_fit`
contract. The full pre-1.0 source is also available in git history at commit `3670edd`.
