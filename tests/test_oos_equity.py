"""Smoke test for the real-data equity OOS harness (non-shipped research; needs pandas + data)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

pytest.importorskip("pandas")
oos_equity = pytest.importorskip("research.oos_equity")


def test_rolling_oos_runs():
    import pandas as pd

    if not oos_equity.DATA.exists():
        pytest.skip("bundled equity data not present")
    # small, fast subset
    R = pd.read_csv(oos_equity.DATA, index_col=0).values[:400, :12]
    fixed, rec, oracle, ew, counts = oos_equity.rolling_oos(
        R, train_len=40, test_len=21, step=42
    )
    assert all(v > 0 for v in (rec, oracle, ew))
    assert rec >= oracle - 1e-9  # the recommender cannot beat the per-window oracle
    assert sum(counts.values()) > 0
    assert "RECOMMENDER" in oos_equity.report(fixed, rec, oracle, ew, counts)
