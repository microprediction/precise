"""Keyed, river-style online covariance for a *dynamic universe* of variables.

In finance the set of variables (tickers, instruments, models) changes over time: new
names enter and old ones leave between observations. :class:`DynamicCovariance` accepts
observations as **dicts keyed by name** (river-style ``update(x)`` / ``learn_one(x)``) and
tracks a covariance estimate whose dimension follows the live universe.

It maintains, for each distinct key-set seen, a *universe* wrapping a (truly online)
positional estimator from this package over a fixed column ordering. A universe is updated
whenever the incoming observation contains all of its keys; otherwise it accrues *staleness*
and is eventually evicted (bounded by ``max_universes`` / ``max_staleness``). No replay
buffers are kept — everything is online. A full matrix is assembled per query by choosing,
for each pair, the longest-lived (and least stale) universe containing both, filling any
gaps with the grand off-diagonal mean and projecting to the nearest positive-definite matrix.
So when a variable drops out, that pair's covariance is still served from the long-lived
universe that has it until a fresher universe overtakes it.

Output is a dict-of-dicts (numpy only); :meth:`to_frame` returns a pandas ``DataFrame`` when
the optional ``[pandas]`` extra is installed.
"""

from __future__ import annotations

import numpy as np

from precise._linalg import cov_to_corrcoef, nearest_pos_def, to_symmetric
from precise.base import BaseOnlineCovariance
from precise.ewa import EwaCovariance


class _Universe:
    """A fixed set of keys with a wrapped online positional estimator. No buffer."""

    def __init__(self, keys, factory):
        self.keys: list[str] = list(keys)
        self.keys_set = set(self.keys)
        self.staleness = 0
        self.longevity = 0
        self._est: BaseOnlineCovariance = factory()

    def update(self, x: dict) -> None:
        y = np.array([x[k] for k in self.keys], dtype=float)
        self._est.partial_fit(y)
        self.staleness = 0
        self.longevity += 1

    @property
    def running_cov(self) -> np.ndarray | None:
        return self._est.covariance_ if self._est.n_samples_ > 0 else None


class DynamicCovariance:
    """Online covariance over a universe whose variables enter and leave over time.

    :param estimator:      A positional online estimator class to use within each universe
                           (default :class:`~precise.ewa.EwaCovariance`).
    :param max_universes:  Maximum number of universes to maintain concurrently.
    :param max_staleness:  Drop a universe after this many updates without usable data.
    :param estimator_kwargs:  Forwarded to ``estimator`` when instantiating each universe.
    """

    def __init__(
        self,
        estimator: type[BaseOnlineCovariance] = EwaCovariance,
        *,
        max_universes: int = 10,
        max_staleness: int = 50,
        **estimator_kwargs,
    ):
        self.estimator = estimator
        self.estimator_kwargs = estimator_kwargs
        self.max_universes = max_universes
        self.max_staleness = max_staleness
        self.states: dict[int, _Universe] = {}
        self.x: dict | None = None
        self._counter = 0

    # ------------------------------------------------------------------ internals
    def _factory(self):
        return lambda: self.estimator(**self.estimator_kwargs)

    def _add_universe(self, universe: _Universe) -> None:
        self.states[self._counter] = universe
        self._counter += 1

    # ----------------------------------------------------------------- streaming
    def update(self, x: dict) -> DynamicCovariance:
        """Update with one keyed observation ``{name: value, ...}``."""
        self.x = dict(x)
        x_keys = set(x.keys())

        for universe in self.states.values():
            if universe.keys_set.issubset(x_keys):
                universe.update(x)
            else:
                universe.staleness += 1

        # Evict universes that have gone stale.
        for ndx in [n for n, u in self.states.items() if u.staleness > self.max_staleness]:
            del self.states[ndx]

        # Start a new universe for an unseen key-set.
        if x_keys not in [u.keys_set for u in self.states.values()]:
            fresh = _Universe(keys=x.keys(), factory=self._factory())
            fresh.update(x)
            self._add_universe(fresh)
            if len(self.states) > self.max_universes:
                # Drop the stalest, then least-long-lived universe.
                victim = sorted(
                    self.states.items(), key=lambda kv: (-kv[1].staleness, kv[1].longevity)
                )[0][0]
                del self.states[victim]
        return self

    # river-compatible aliases
    def learn_one(self, x: dict) -> DynamicCovariance:
        return self.update(x)

    def learn_many(self, X) -> DynamicCovariance:
        for x in X:
            self.update(x)
        return self

    # ---------------------------------------------------------------- assembly
    def _resolve_keys(self, keys) -> list[str]:
        if keys is not None:
            return list(keys)
        if self.x is None:
            raise ValueError("No keys supplied and no observation has been seen yet.")
        return list(self.x.keys())

    def _pairwise(self, keys: list[str]) -> np.ndarray:
        n = len(keys)
        idx = {k: i for i, k in enumerate(keys)}
        M = np.full((n, n), np.nan)
        for i, ki in enumerate(keys):
            for kj in keys[i:]:
                candidates = [
                    u
                    for u in self.states.values()
                    if {ki, kj}.issubset(u.keys_set) and u.running_cov is not None
                ]
                if candidates:
                    # Prefer the longest-lived universe, breaking ties towards the freshest.
                    u = max(candidates, key=lambda u: (u.longevity, -u.staleness))
                    cov = u.running_cov
                    assert cov is not None  # guaranteed by the candidate filter
                    a, b = u.keys.index(ki), u.keys.index(kj)
                    value = cov[a, b]
                    M[idx[ki], idx[kj]] = value
                    M[idx[kj], idx[ki]] = value
        return M

    def cov_array(self, keys=None):
        """Return ``(matrix, keys)``: a nearest-positive-definite covariance ndarray."""
        keys = self._resolve_keys(keys)
        M = self._pairwise(keys)
        off_diag = M[~np.eye(len(keys), dtype=bool)]
        fill = np.nanmean(off_diag) if np.any(~np.isnan(off_diag)) else 0.0
        if np.isnan(fill):
            fill = 0.0
        M = np.where(np.isnan(M), fill, M)
        return nearest_pos_def(to_symmetric(M)), keys

    def get_cov(self, keys=None) -> np.ndarray:
        return self.cov_array(keys)[0]

    def get_corr(self, keys=None) -> np.ndarray:
        cov, _ = self.cov_array(keys)
        corr = cov_to_corrcoef(cov)
        np.fill_diagonal(corr, 1.0)
        return corr

    @staticmethod
    def _as_dict_of_dicts(matrix: np.ndarray, keys: list[str]) -> dict[str, dict[str, float]]:
        return {
            ki: {kj: float(matrix[i, j]) for j, kj in enumerate(keys)}
            for i, ki in enumerate(keys)
        }

    # ------------------------------------------------------- fitted attributes
    @property
    def covariance_(self) -> dict[str, dict[str, float]]:
        cov, keys = self.cov_array()
        return self._as_dict_of_dicts(cov, keys)

    @property
    def correlation_(self) -> dict[str, dict[str, float]]:
        keys = self._resolve_keys(None)
        return self._as_dict_of_dicts(self.get_corr(keys), keys)

    # river-compatible alias
    covariance = covariance_

    def to_frame(self, keys=None):
        """Return the covariance as a pandas ``DataFrame`` (requires the ``[pandas]`` extra)."""
        try:
            import pandas as pd
        except ImportError as exc:  # pragma: no cover - exercised only without pandas
            raise ImportError(
                "to_frame requires pandas. Install with: pip install precise[pandas]"
            ) from exc
        cov, keys = self.cov_array(keys)
        return pd.DataFrame(cov, index=keys, columns=keys)

    def __repr__(self) -> str:
        return (
            f"DynamicCovariance(estimator={self.estimator.__name__}, "
            f"universes={len(self.states)})"
        )
