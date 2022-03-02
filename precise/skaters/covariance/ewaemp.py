from precise.skaters.covariance.ewaempfactory import ewa_emp_pcov_factory
from precise.skaters.covarianceutil.conventions import Y_DATA_TYPE
from precise.skaters.covarianceutil.differencing import d1_factory


def ewa_emp_pcov_d0_r01(y, s, k=1, e=1):
    return ewa_emp_pcov_factory(y=y, s=s, k=k, r=0.01)


def ewa_emp_pcov_d0_r02(y, s, k=1, e=1):
    return ewa_emp_pcov_factory(y=y, s=s, k=k, r=0.02)


def ewa_emp_pcov_d0_r05(y, s, k=1, e=1):
    return ewa_emp_pcov_factory(y=y, s=s, k=k, r=0.05)


def ewa_emp_pcov_d0_r10(y, s, k=1, e=1):
    return ewa_emp_pcov_factory(y=y, s=s, k=k, r=0.10)


EMA_DO_COV_SKATERS = [ewa_emp_pcov_d0_r01, ewa_emp_pcov_d0_r02, ewa_emp_pcov_d0_r05, ewa_emp_pcov_d0_r10]


def ewa_emp_pcov_d1_r01(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    """
        For when changes are iid gaussian
    """
    return d1_factory(f = ewa_emp_pcov_d0_r01, y=y, s=s, k=k)


def ewa_emp_pcov_d1_r02(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    return d1_factory(f = ewa_emp_pcov_d0_r02, y=y, s=s, k=k)


def ewa_emp_pcov_d1_r05(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    return d1_factory(f = ewa_emp_pcov_d0_r05, y=y, s=s, k=k)


def ewa_emp_pcov_d1_r10(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    return d1_factory(f = ewa_emp_pcov_d0_r10, y=y, s=s, k=k)


EXP_EMP_D1_COV_SKATERS = [ewa_emp_pcov_d1_r01, ewa_emp_pcov_d1_r02, ewa_emp_pcov_d1_r05, ewa_emp_pcov_d1_r10]

