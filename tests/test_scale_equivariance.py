"""Covariance estimates must not depend on the units of the input.

Two absolute epsilons in `_linalg.py` decided the answer whenever the data was small: an additive
`+ EPS` in the correlation denominator, and an absolute eigenvalue floor in `make_pos_def`. Both
have units of variance, so both stop being negligible at exactly the scale a user in basis points
or log-returns works at. Found by audit.
"""

import numpy as np
import pytest

from precise import (
    BlockCovariance,
    EwaCovariance,
    LedoitWolfCovariance,
    SchurCovariance,
    SchurLedoitWolfCovariance,
)

SCALES = [1e0, 1e-3, 1e-6, 1e-9]


def _stream(cls, X):
    est = cls()
    for row in X:
        est.partial_fit(row)
    return est


@pytest.mark.parametrize(
    "cls",
    [
        EwaCovariance,
        LedoitWolfCovariance,
        BlockCovariance,
        SchurCovariance,
        SchurLedoitWolfCovariance,
    ],
)
@pytest.mark.parametrize("scale", SCALES)
def test_correlation_keeps_its_unit_diagonal_at_any_scale(cls, scale):
    rng = np.random.default_rng(2)
    X = rng.standard_normal((200, 5)) * scale
    diagonal = np.diag(_stream(cls, X).correlation_)
    assert np.allclose(diagonal, 1.0, atol=1e-8), (
        f"{cls.__name__} at scale {scale:g}: correlation diagonal {diagonal.min():.4f}, "
        "which is a property of the units rather than of the data"
    )


@pytest.mark.parametrize(
    "cls", [BlockCovariance, SchurCovariance, SchurLedoitWolfCovariance]
)
@pytest.mark.parametrize("scale", [1e-6, 1e-9])
def test_the_estimate_tracks_the_data_scale(cls, scale):
    # These returned `1e-8 * I` below a data scale of about 1e-4 — up to nine thousand times the
    # true variance, carrying no correlation information at all.
    rng = np.random.default_rng(1)
    X = rng.standard_normal((300, 6)) * scale
    got = float(np.trace(_stream(cls, X).covariance_))
    truth = float(np.trace(np.cov(X.T)))
    assert 0.25 * truth <= got <= 4.0 * truth, (
        f"{cls.__name__} at scale {scale:g}: trace {got:.3e} against a true {truth:.3e}"
    )
