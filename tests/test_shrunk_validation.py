"""ShrunkCovariance must reject a target or intensity outside its documented domain.

Any unrecognised ``target`` (a typo such as ``"identitiy"``) silently selected the constant
correlation target, and ``delta`` outside ``[0, 1]`` extrapolated past the convex combination and
returned an indefinite matrix with negative "squared" Mahalanobis distances. (#104)
"""

import numpy as np
import pytest

from precise import ShrunkCovariance


def _data(seed=20260926):
    rng = np.random.default_rng(seed)
    true = np.full((4, 4), 0.9)
    np.fill_diagonal(true, 1.0)
    return rng.multivariate_normal(np.zeros(4), true, size=1000)


@pytest.mark.parametrize("target", ["identitiy", "Identity", None, "", 0])
def test_unknown_target_is_rejected_not_read_as_constant_correlation(target):
    with pytest.raises(ValueError, match="target must be one of"):
        ShrunkCovariance(target=target)


@pytest.mark.parametrize("delta", [-1.0, -1e-9, 1.0 + 1e-9, 2.0, float("nan"), float("inf"), None])
def test_intensity_outside_unit_interval_is_rejected(delta):
    with pytest.raises(ValueError, match="delta must be"):
        ShrunkCovariance(delta=delta)


@pytest.mark.parametrize("target", ["identity", "constant_correlation"])
@pytest.mark.parametrize("delta", [0.0, 0.5, 1.0])
def test_documented_configurations_stay_psd(target, delta):
    X = _data()
    est = ShrunkCovariance(r=0.05, delta=delta, target=target).fit(X)
    assert np.min(np.linalg.eigvalsh(est.covariance_)) > 0
    assert np.min(est.mahalanobis(X)) >= 0


def test_identity_and_constant_correlation_targets_differ():
    # The two documented targets must give different answers on correlated data; a typo used to
    # land on constant correlation exactly.
    X = _data()
    ident = ShrunkCovariance(r=0.05, delta=0.5, target="identity").fit(X).covariance_
    const = ShrunkCovariance(r=0.05, delta=0.5, target="constant_correlation").fit(X).covariance_
    assert np.linalg.norm(ident - const) > 0.1 * np.linalg.norm(ident)


def test_set_params_and_direct_assignment_are_checked_before_the_state_is_used():
    est = ShrunkCovariance().fit(_data())
    with pytest.raises(ValueError):
        est.set_params(delta=2.0)
    assert est.delta == 0.1
    with pytest.raises(ValueError):
        est.set_params(target="identitiy")
    assert est.target == "constant_correlation"
    est.delta = 2.0  # bypasses set_params; reading the estimate must still refuse
    with pytest.raises(ValueError, match="delta must be"):
        _ = est.covariance_
