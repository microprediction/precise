"""Regression coverage for current-universe retention at the capacity boundary (#81)."""

import numpy as np
import pytest

from precise import DynamicUniverse, EmpiricalCovariance, keyed


@pytest.mark.parametrize("capacity", [1, 2, 10])
@pytest.mark.parametrize("method", ["update", "learn_one"])
def test_nested_expansion_learns_new_names_at_capacity(capacity, method):
    d = DynamicUniverse(EmpiricalCovariance(), max_universes=capacity)
    # Fill the cache with increasingly large, live subsets.
    for size in range(1, capacity + 1):
        for t in range(8):
            getattr(d, method)({f"k{i}": float((i + 1) * t) for i in range(size)})
    rows = np.random.default_rng(81).normal(size=(40, capacity + 1))
    keys = [f"k{i}" for i in range(capacity + 1)]
    for n, row in enumerate(rows, 1):
        getattr(d, method)(dict(zip(keys, row)))
        assert len(d.states) <= capacity
        current = [u for u in d.states.values() if u.keys_set == set(keys)]
        assert len(current) == 1
        assert current[0].longevity == n
    # The entrant's marginal and pair entries come from actual accumulated observations.
    expected = np.cov(rows, rowvar=False, bias=True)
    actual = d.get_cov(keys)
    np.testing.assert_allclose(actual[-1], expected[-1], rtol=1e-12, atol=1e-12)


def test_retention_keeps_existing_eviction_priority():
    d = DynamicUniverse(EmpiricalCovariance(), max_universes=3, max_staleness=100)
    for _ in range(5):
        d.update({"A": 1.0})
    for _ in range(3):
        d.update({"A": 1.0, "B": 2.0})
    d.update({"C": 3.0})
    # A and AB have the same staleness; the younger AB must still be evicted first.
    d.update({"D": 4.0})
    assert {frozenset(u.keys) for u in d.states.values()} == {
        frozenset("A"),
        frozenset("C"),
        frozenset("D"),
    }


def test_staleness_eviction_still_precedes_capacity_selection():
    d = DynamicUniverse(EmpiricalCovariance(), max_universes=2, max_staleness=0)
    d.update({"A": 1.0})
    d.update({"B": 2.0})
    assert [u.keys for u in d.states.values()] == [["B"]]


@pytest.mark.parametrize("capacity", [1, 2, 10, np.int64(2)])
def test_positive_integer_capacity_supported(capacity):
    d = keyed(EmpiricalCovariance(), dynamic=True, max_universes=capacity)
    d.update({"A": 1.0})
    assert len(d.states) == 1


@pytest.mark.parametrize("capacity", [0, -1, 1.5, 2.0, True, False, None, "2", np.nan])
def test_invalid_capacity_rejected(capacity):
    with pytest.raises(ValueError, match="max_universes must be a positive integer"):
        DynamicUniverse(EmpiricalCovariance(), max_universes=capacity)
