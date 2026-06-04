"""Empirical (sample) online covariance.

Running population covariance via Welford's algorithm (``window=None``), or a rolling
window of the most recent ``window`` observations. Matches ``numpy.cov(..., bias=True)``
and sklearn's empirical-covariance (MLE) convention.
"""

from __future__ import annotations

import numpy as np

from precise._state import emp_init, emp_update
from precise.base import BaseOnlineCovariance


class EmpiricalCovariance(BaseOnlineCovariance):
    """Online empirical covariance.

    :param window:  If ``None`` (default), maintain a running estimate over all observations.
                    If an int, estimate over a rolling window of the most recent ``window``.
    :param diff:    If ``True``, estimate the covariance of first differences of the stream
                    (useful when levels are integrated but changes are iid).
    """

    def __init__(self, window: int = None, diff: bool = False):
        self.window = window
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        s = emp_init(n_dim)
        if self.window is not None:
            s["buffer"] = []
        return s

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        if self.window is None:
            return emp_update(s, x)

        buffer = list(s["buffer"])
        buffer.append(np.asarray(x, dtype=float).tolist())
        if len(buffer) > self.window:
            buffer = buffer[-self.window :]
        rows = np.array(buffer, dtype=float)
        mean = rows.mean(axis=0)
        if len(buffer) >= 2:
            cov = np.atleast_2d(np.cov(rows, rowvar=False, bias=True))
        else:
            cov = np.zeros((s["n_dim"], s["n_dim"]))
        return {
            "n_dim": s["n_dim"],
            "n_samples": s["n_samples"] + 1,
            "mean": mean,
            "cov": cov,
            "buffer": buffer,
        }
