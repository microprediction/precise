"""Tests for the keyed river-style adapters: keyed(), FixedUniverse, DynamicUniverse."""

import numpy as np
import pytest

from precise import (
    DynamicUniverse,
    EmpiricalCovariance,
    FixedUniverse,
    HuberCovariance,
    keyed,
)


def _stream(keys, n, rng):
    for _ in range(n):
        yield {k: float(rng.standard_normal()) for k in keys}


def test_keyed_front_door_dispatch():
    assert isinstance(keyed(EmpiricalCovariance()), FixedUniverse)
    assert isinstance(keyed(EmpiricalCovariance(), dynamic=True), DynamicUniverse)
    # default wrapped estimator when none supplied
    assert isinstance(keyed(), FixedUniverse)


def test_wraps_a_configured_instance_and_clones_it():
    proto = HuberCovariance(c=3.0)
    d = keyed(proto, dynamic=True)
    rng = np.random.default_rng(0)
    for x in _stream(["A", "B", "C"], 80, rng):
        d.learn_one(x)
    # the prototype itself is never fitted; each universe holds its own clone
    assert proto.n_samples_ == 0
    assert set(d.covariance_.keys()) == {"A", "B", "C"}


def test_class_form_still_works():
    d = keyed(EmpiricalCovariance, dynamic=True, max_staleness=10)
    rng = np.random.default_rng(0)
    for x in _stream(["A", "B"], 40, rng):
        d.update(x)
    assert set(d.covariance_.keys()) == {"A", "B"}
    # estimator kwargs are rejected when an instance (not a class) is given
    with pytest.raises(ValueError):
        keyed(EmpiricalCovariance(), r=0.1)


def test_fixed_universe_stable_keys_matches_positional():
    rng = np.random.default_rng(1)
    rows = rng.standard_normal((400, 3))
    k = keyed(EmpiricalCovariance())
    for row in rows:
        k.update({"A": row[0], "B": row[1], "C": row[2]})
    cov = k.covariance_
    assert set(cov) == {"A", "B", "C"}
    expected = np.cov(rows, rowvar=False, bias=True)
    assert cov["A"]["B"] == pytest.approx(expected[0, 1], abs=1e-8)
    arr = k.get_cov(["A", "B", "C"])
    assert np.allclose(arr, expected, atol=1e-8)


def test_fixed_universe_imputes_missing_key():
    k = FixedUniverse(EmpiricalCovariance(), impute="ffill")
    k.update({"A": 1.0, "B": 2.0})
    k.update({"A": 1.5})  # B missing -> forward-filled to 2.0, no crash
    k.update({"A": 0.5, "B": 1.0})
    cov = k.covariance_
    assert set(cov) == {"A", "B"}  # universe fixed from first observation
    assert np.isfinite(cov["B"]["B"])


def test_dynamic_universe_variables_enter_and_leave():
    rng = np.random.default_rng(2)
    d = DynamicUniverse(EmpiricalCovariance(), max_staleness=100)
    for x in _stream(["A", "B", "C", "D"], 60, rng):
        d.update(x)
    for x in _stream(["B", "C", "D", "E"], 60, rng):  # A leaves, E enters
        d.update(x)
    cov = d.covariance_
    assert set(cov) == {"B", "C", "D", "E"}
    assert np.isfinite(cov["B"]["C"])
    assert np.isfinite(cov["E"]["E"])


def test_river_aliases_and_pd_output():
    rng = np.random.default_rng(3)
    d = keyed(EmpiricalCovariance(), dynamic=True)
    for x in _stream(["X", "Y", "Z"], 100, rng):
        d.learn_one(x)
    assert d.covariance == d.covariance_  # river-style .covariance alias
    arr = d.get_cov(["X", "Y", "Z"])
    assert np.min(np.linalg.eigvalsh(arr)) > 0  # nearest-PD assembly
