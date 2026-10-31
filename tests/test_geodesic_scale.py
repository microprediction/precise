"""Regression coverage for the dimensional eigenvalue floor in #108."""

import numpy as np
import pytest

from precise import SchurCovariance
from precise._linalg import geodesic_step, make_pos_def
from precise.assessment import SchurLikelihood

START = np.array([[2.0, 0.3], [0.3, 1.0]])
END = np.array([[1.0, 0.6], [0.6, 3.0]])


@pytest.mark.parametrize("scale", [1e-18, 1e-14, 1.0, 1e12])
@pytest.mark.parametrize("gamma", [0.0, 0.25, 0.5, 1.0])
def test_geodesic_homogeneity(scale, gamma):
    expected = geodesic_step(START, END, gamma)
    actual = geodesic_step(scale * START, scale * END, gamma) / scale
    np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-12)


@pytest.mark.parametrize("scale", [1e-18, 1e-14, 1.0])
@pytest.mark.parametrize("gamma", [0.0, 1.0])
def test_geodesic_endpoints(scale, gamma):
    expected = make_pos_def(START if gamma == 0 else END)
    actual = geodesic_step(scale * START, scale * END, gamma) / scale
    np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-12)


@pytest.mark.parametrize("data_scale", [1e-7, 1e-9])
@pytest.mark.parametrize("gamma", [0.0, 0.5, 1.0])
def test_public_schur_covariance_homogeneity(data_scale, gamma):
    X = np.random.default_rng(8).normal(size=(100, 4))
    kwargs = dict(r=0.05, n_blocks=2, gamma=gamma, interpolation="geodesic")
    expected = SchurCovariance(**kwargs).fit(X).covariance_
    actual = SchurCovariance(**kwargs).fit(data_scale * X).covariance_ / data_scale**2
    np.testing.assert_allclose(actual, expected, rtol=1e-11, atol=1e-11)


@pytest.mark.parametrize("scale", [1e-18, 1e-14])
@pytest.mark.parametrize("gamma", [0.0, 0.5, 1.0])
def test_public_schur_likelihood_unit_change(scale, gamma):
    X = np.random.default_rng(9).normal(size=(100, 2))
    assessor = SchurLikelihood(gamma=gamma, n_blocks=2, interpolation="geodesic")
    expected = assessor.score(END, X_test=X)
    actual = assessor.score(scale * END, X_test=np.sqrt(scale) * X)
    # A p-dimensional Gaussian log density shifts by -(p/2) log(scale).
    np.testing.assert_allclose(actual + len(END) / 2 * np.log(scale), expected, atol=1e-11)
