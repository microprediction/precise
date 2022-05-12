from precise.skaters.covariance.weakfactory import weak_pcov_factory
from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r01, ewa_emp_pcov_d1_r02, ewa_emp_pcov_d1_r05
from precise.skaters.covariance.ewalw import ewa_lw_scov_d0_r01, ewa_lw_scov_d0_r02, ewa_lw_scov_d0_r05


# Using moving averages

def weak_ewa_emp_pcov_d0_r01(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_emp_pcov_d0_r01, s=s, y=y, k=k, e=e)


def weak_ewa_emp_pcov_d1_r02(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_emp_pcov_d1_r02, s=s, y=y, k=k, e=e)


def weak_ewa_emp_pcov_d1_r05(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_emp_pcov_d1_r05, s=s, y=y, k=k, e=e)


# Using online Ledoit-Wolf

def weak_ewa_lw_scov_d0_r01(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_lw_scov_d0_r01, s=s, y=y, k=k, e=e)


def weak_ewa_lw_scov_d0_r02(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_lw_scov_d0_r02, s=s, y=y, k=k, e=e)


def weak_ewa_lw_scov_d0_r05(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_lw_scov_d0_r05, s=s, y=y, k=k, e=e)


WEAK_EWA_DO_COV_SKATERS = [ weak_ewa_emp_pcov_d0_r01,weak_ewa_emp_pcov_d1_r02, weak_ewa_emp_pcov_d1_r05,
                           weak_ewa_lw_scov_d0_r01,weak_ewa_lw_scov_d0_r02,weak_ewa_lw_scov_d0_r05]