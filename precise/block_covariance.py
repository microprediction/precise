"""Memory-efficient block-diagonal online covariance.

Tracks only the within-block (contiguous ``n_blocks``) recency-weighted covariances, so the
running state and per-step cost scale with the block size ``b`` rather than the dimension
``p``: roughly ``O(p*b)`` memory and work per observation, versus ``O(p^2)`` for a dense
estimator. Cross-block entries are zero -- this is the memory-light, ``gamma=0``
(block-diagonal / composite) member of the Schur family, intended for very high ``p`` where
the dense ``p x p`` covariance is expensive or impossible to hold while streaming. A
block-diagonal of positive-definite blocks is positive-definite, so no global
eigen-projection (``O(p^3)``) is needed, and the precision is likewise block-wise. numpy only.

Relative to ``SchurCovariance(gamma=0)`` (which keeps the full ``p x p`` EWA covariance and
zeroes the cross-block entries only at read time), this never allocates the dense matrix in
its state; it densifies only on a ``covariance_`` request. See microprediction/precise#47.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import make_pos_def, to_symmetric
from precise._state import ewa_burn_n, ewa_init, ewa_update
from precise.base import BaseOnlineCovariance


class BlockCovariance(BaseOnlineCovariance):
    """Online block-diagonal covariance with ``O(p*b)`` state.

    :param r:         Weight of the most recent observation (decay rate), in (0, 1].
    :param n_blocks:  Number of contiguous blocks to partition the variables into.
    :param diff:      If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, n_blocks: int = 4, diff: bool = False):
        self.r = r
        self.n_blocks = n_blocks
        self.diff = diff
        super().__init__()

    def _slices(self, n_dim: int) -> list[tuple[int, int]]:
        nb = min(max(1, self.n_blocks), n_dim)
        return [(int(idx[0]), int(idx[-1]) + 1) for idx in np.array_split(np.arange(n_dim), nb)]

    def _init_state(self, n_dim: int) -> dict:
        sl = self._slices(n_dim)
        return {
            "n_dim": n_dim,
            "n_samples": 0,
            "r": float(self.r),
            "n_burn": ewa_burn_n(self.r),
            "slices": sl,
            "subs": [ewa_init(b - a, self.r) for a, b in sl],
        }

    def _update_state(self, s: dict, x: np.ndarray) -> dict:
        subs = []
        for sub, (a, b) in zip(s["subs"], s["slices"]):
            sub = {**sub, "mean": np.asarray(sub["mean"], dtype=float),
                   "cov": np.asarray(sub["cov"], dtype=float)}
            subs.append(ewa_update(sub, x[a:b]))
        return {**s, "n_samples": s["n_samples"] + 1, "subs": subs}

    def _state_to_cov(self, state: dict) -> np.ndarray:
        p = state["n_dim"]
        out = np.zeros((p, p))
        for sub, (a, b) in zip(state["subs"], state["slices"]):
            out[a:b, a:b] = make_pos_def(to_symmetric(np.asarray(sub["cov"], dtype=float)))
        return out

    def _state_to_mean(self, state: dict) -> np.ndarray:
        m = np.zeros(state["n_dim"])
        for sub, (a, b) in zip(state["subs"], state["slices"]):
            m[a:b] = np.asarray(sub["mean"], dtype=float)
        return m

    # The state holds a list of per-block sub-dicts (nested arrays), so we serialize it
    # explicitly to flat JSON rather than relying on the base list/array coercion.
    def get_state(self) -> dict | None:
        if self._state is None:
            return None
        s = self._state
        return {
            "n_dim": int(s["n_dim"]),
            "n_samples": int(s["n_samples"]),
            "r": float(s["r"]),
            "n_burn": int(s["n_burn"]),
            "slices": [[int(a), int(b)] for a, b in s["slices"]],
            "block_means": [np.asarray(sub["mean"], dtype=float).tolist() for sub in s["subs"]],
            "block_covs": [np.asarray(sub["cov"], dtype=float).tolist() for sub in s["subs"]],
        }

    def set_state(self, state: dict | None) -> BaseOnlineCovariance:
        if state is None:
            self._state = None
            self.n_features_in_ = None
            return self
        n_samples, r, n_burn = int(state["n_samples"]), float(state["r"]), int(state["n_burn"])
        slices = [(int(a), int(b)) for a, b in state["slices"]]
        subs = [
            {"n_dim": b - a, "n_samples": n_samples, "r": r, "n_burn": n_burn,
             "mean": np.asarray(m, dtype=float), "cov": np.asarray(c, dtype=float)}
            for (a, b), m, c in zip(slices, state["block_means"], state["block_covs"])
        ]
        self._state = {"n_dim": int(state["n_dim"]), "n_samples": n_samples, "r": r,
                       "n_burn": n_burn, "slices": slices, "subs": subs}
        self.n_features_in_ = int(state["n_dim"])
        return self
