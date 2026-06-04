"""Empirical (sample) online covariance.

Running population covariance via Welford's algorithm — a true O(1)-per-step incremental
update with no stored window. Matches ``numpy.cov(..., bias=True)`` and sklearn's
empirical-covariance (MLE) convention.
"""

from __future__ import annotations

import numpy as np

from precise._state import emp_init, emp_update
from precise.base import BaseOnlineCovariance


class EmpiricalCovariance(BaseOnlineCovariance):
    """Online empirical covariance over the full history seen so far.

    :param diff:  If ``True``, estimate the covariance of first differences of the stream
                  (useful when levels are integrated but changes are iid).
    """

    def __init__(self, diff: bool = False):
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return emp_init(n_dim)

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        return emp_update(s, x)
