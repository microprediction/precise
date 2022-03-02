from precise.skaters.covariance.ewalwfactory import ewa_lw_scov_factory
from precise.skaters.covarianceutil.differencing import d1_factory

# EWALD short for "Exp Weight Avg" Ledoit-Wolf

# Experimental estimator inspired by Ledoit-Wolf
# Keeps a buffer of last n_buffer observations
# Tracks quantities akin to a^2, d^2 used by LW to
# estimate a "reasonable" linear shrinkage


def ewa_lw_scov_d0_r01(y, s, k=1, e=1):
    assert k==1
    return ewa_lw_scov_factory(y=y, s=s, r=0.01, e=e)


def ewa_lw_scov_d0_r02(y, s, k=1, e=1):
    assert k==1
    return ewa_lw_scov_factory(y=y, s=s, r=0.02)


def ewa_lw_scov_d0_r05(y, s, k=1, e=1):
    assert k==1
    return ewa_lw_scov_factory(y=y, s=s, r=0.05)



EWA_LW_D0_COV_SKATERS = [ewa_lw_scov_d0_r01, ewa_lw_scov_d0_r02 ]


def ewa_lw_scov_d1_r01(y, s, k=1, e=1):
    assert k == 1
    return d1_factory( f=ewa_lw_scov_factory, y=y, s=s, r=0.01)


def ewa_lw_scov_d1_r02(y, s, k=1, e=1):
    assert k == 1
    return d1_factory( f=ewa_lw_scov_factory, y=y, s=s, r=0.02)


EWA_LW_D1_COV_SKATERS = [ewa_lw_scov_d1_r01, ewa_lw_scov_d1_r02 ]