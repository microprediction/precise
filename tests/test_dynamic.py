"""Tests for the keyed, dynamic-universe DynamicCovariance layer."""

import numpy as np
import pytest

from precise import DynamicCovariance, EmpiricalCovariance


def _stream(keys, n, rng):
    for _ in range(n):
        yield {k: float(rng.standard_normal()) for k in keys}


def test_stable_universe_dict_of_dicts():
    rng = np.random.default_rng(0)
    d = DynamicCovariance(EmpiricalCovariance)
    for x in _stream(["A", "B", "C"], 200, rng):
        d.update(x)
    cov = d.covariance_
    assert set(cov.keys()) == {"A", "B", "C"}
    assert set(cov["A"].keys()) == {"A", "B", "C"}
    # symmetric
    assert cov["A"]["B"] == pytest.approx(cov["B"]["A"])
    # positive definite array form
    arr = d.get_cov(["A", "B", "C"])
    assert np.min(np.linalg.eigvalsh(arr)) > 0


def test_variables_enter_and_leave():
    rng = np.random.default_rng(1)
    d = DynamicCovariance(EmpiricalCovariance, max_staleness=5)
    # Phase 1: A,B,C,D alive.
    for x in _stream(["A", "B", "C", "D"], 60, rng):
        d.update(x)
    # Phase 2: A leaves, E enters; B,C,D persist.
    for x in _stream(["B", "C", "D", "E"], 60, rng):
        d.update(x)

    cov = d.covariance_
    assert set(cov.keys()) == {"B", "C", "D", "E"}, "live universe should track current keys"
    # A pair alive together in both phases is recoverable.
    assert np.isfinite(cov["B"]["C"])
    # The newly arrived variable is present and self-consistent.
    assert np.isfinite(cov["E"]["E"])
    # Can still query the historical pair explicitly.
    arr = d.get_cov(["B", "C", "D"])
    assert arr.shape == (3, 3)


def test_river_aliases():
    rng = np.random.default_rng(2)
    d = DynamicCovariance(EmpiricalCovariance)
    for x in _stream(["X", "Y"], 50, rng):
        d.learn_one(x)
    d.learn_many(list(_stream(["X", "Y"], 50, rng)))
    assert set(d.covariance.keys()) == {"X", "Y"}  # river-style .covariance alias
    assert d.covariance == d.covariance_


def test_overlap_clone_preserves_pairs():
    rng = np.random.default_rng(3)
    d = DynamicCovariance(EmpiricalCovariance, min_longevity_for_clone=2, max_staleness=100)
    for x in _stream(["A", "B", "C", "D", "E"], 40, rng):
        d.update(x)
    # Drop one key -> high overlap -> should clone the survivors rather than discard history.
    for x in _stream(["A", "B", "C", "D"], 40, rng):
        d.update(x)
    cov = d.covariance_
    assert set(cov.keys()) == {"A", "B", "C", "D"}
    assert len(d.states) >= 2, "an overlapping subset universe should have been cloned"
