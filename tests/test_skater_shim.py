"""The removed skater API should fail with a helpful, actionable message."""

import importlib

import pytest


def test_importing_skaters_raises_actionable_error():
    with pytest.raises(ImportError) as exc:
        importlib.import_module("precise.skaters")
    msg = str(exc.value)
    assert "removed in precise 1.0" in msg
    assert "MIGRATING.md" in msg
    assert "EwaCovariance" in msg


def test_from_skaters_import_also_raises():
    with pytest.raises(ImportError):
        exec("from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r005")


def test_core_package_still_imports_fine():
    # The shim must not affect the real package surface.
    import precise

    assert "EwaCovariance" in precise.estimator_names()
