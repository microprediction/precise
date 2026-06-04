# research

Not shipped with the package (excluded from the wheel/sdist and from the test suite). This is the
home of the benchmarking / elo bake-offs that compare covariance estimators against ground truth.

The intended modern workflow uses the sibling [`randomcov`](https://github.com/microprediction/randomcov)
package to generate ground-truth covariance matrices, samples from them, streams the samples through
every estimator in `precise.all_estimators()`, and scores the recovery (likelihood, min-variance
performance, Frobenius error). Install the extras with:

```bash
pip install -e ".[research]"
```

## `legacy_skatervaluation/`

The original elo bake-off harness, **targeting the pre-1.0 functional "skater" API** (and importing
the now-removed `precise.skaters` / `precise.skatertools` modules). Preserved for reference; it does
not run against precise 1.0 and is pending a rewrite to the `all_estimators()` / `partial_fit`
contract. The full pre-1.0 source is also available in git history at commit `3670edd`.
