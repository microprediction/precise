"""Tests for ConditionalCovariance (vol x corr composition) and the from_skater adapter."""

import math
import pickle

import numpy as np
import pytest

from precise import (
    ConditionalCovariance,
    EwaCovariance,
    LedoitWolfCovariance,
    from_skater,
    keyed,
)


def _data(n=40_000, seed=0):
    rng = np.random.default_rng(seed)
    vols = np.array([1.0, 3.0])
    corr = np.array([[1.0, 0.6], [0.6, 1.0]])
    cov = np.diag(vols) @ corr @ np.diag(vols)
    return rng.multivariate_normal([0, 0], cov, size=n), vols, corr


def test_default_recovers_correlation_and_vols():
    # ConditionalCovariance() with EWA vol + EWA corr is the DCC special case.
    X, vols, corr = _data()
    est = ConditionalCovariance(EwaCovariance(r=0.01), EwaCovariance(r=0.01)).fit(X)
    assert est.correlation_[0, 1] == pytest.approx(0.6, abs=0.1)
    assert np.allclose(np.diag(est.correlation_), 1.0)
    assert np.sqrt(np.diag(est.covariance_)) == pytest.approx(vols, rel=0.15)


def test_composes_robust_vol_with_shrunk_corr():
    X, _, _ = _data(n=5000, seed=1)
    est = ConditionalCovariance(vol=EwaCovariance(r=0.02), corr=LedoitWolfCovariance(r=0.05)).fit(X)
    C = est.covariance_
    assert np.allclose(C, C.T)
    assert np.min(np.linalg.eigvalsh(C)) > 0
    assert np.allclose(np.diag(est.correlation_), 1.0)


# --- a self-contained fake skater to exercise from_skater without the real dependency ---
class _FakeDist:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std


def _fake_skater(y, state):
    """A tiny EWMA vol skater matching the skaters signature f(y, state) -> (dists, state)."""
    if state is None:
        state = {"mean": 0.0, "var": 1.0, "n": 0}
    n = state["n"] + 1
    r = 0.1
    dev = y - state["mean"]
    if n <= 10:
        mean = state["mean"] + dev / n
        var = state["var"] if n == 1 else (state["var"] * (n - 1) + dev * dev) / n
    else:
        mean = (1 - r) * state["mean"] + r * y
        var = (1 - r) * state["var"] + r * dev * dev
    new = {"mean": mean, "var": max(var, 1e-9), "n": n}
    return [_FakeDist(mean, math.sqrt(new["var"]))], new


def test_from_skater_adapter_runs_and_recovers_vols():
    X, vols, _ = _data(n=20_000, seed=2)
    est = ConditionalCovariance(vol=from_skater(_fake_skater), corr=EwaCovariance(r=0.01)).fit(X)
    C = est.covariance_
    assert np.min(np.linalg.eigvalsh(C)) > 0
    assert np.sqrt(np.diag(C)) == pytest.approx(vols, rel=0.2)
    assert est.correlation_[0, 1] == pytest.approx(0.6, abs=0.15)


def test_pickle_roundtrip():
    X, _, _ = _data(n=2000, seed=3)
    est = ConditionalCovariance(vol=from_skater(_fake_skater)).fit(X)
    restored = pickle.loads(pickle.dumps(est))
    assert np.allclose(restored.covariance_, est.covariance_)


def test_get_state_not_supported():
    est = ConditionalCovariance().fit(_data(n=500)[0])
    with pytest.raises(NotImplementedError):
        est.get_state()


def test_composes_with_keyed_adapter():
    # ConditionalCovariance is itself a positional estimator, so keyed() can wrap it.
    rng = np.random.default_rng(4)
    d = keyed(ConditionalCovariance(EwaCovariance(r=0.05), EwaCovariance(r=0.05)), dynamic=True)
    for _ in range(300):
        d.update({"A": float(rng.standard_normal()), "B": float(rng.standard_normal())})
    cov = d.covariance_
    assert set(cov) == {"A", "B"}
    assert np.isfinite(cov["A"]["B"])
