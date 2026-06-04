"""Online location (centre) primitives: running mean and an approximate running median.

The mean is maintained inline by the covariance state updates in ``_state``; this module
holds the standalone primitives reused by robust estimators (e.g. the Huber family,
which centres on a running median rather than the mean).
"""

from __future__ import annotations

import numpy as np


def running_mean_update(mean: np.ndarray, x: np.ndarray, count: int) -> np.ndarray:
    """Incremental sample mean after observing ``x`` as the ``count``-th observation."""
    return mean + (x - mean) / count


def running_median_update(
    median: np.ndarray, x: np.ndarray, step: float
) -> np.ndarray:
    """Approximate online (marginal) median via a small fixed step in the sign direction.

    A lightweight stochastic-approximation median tracker: each coordinate moves by
    ``step`` towards the observation. Cheap, robust to outliers, and adequate for
    centring robust covariance estimators.
    """
    return median + step * np.sign(x - median)
