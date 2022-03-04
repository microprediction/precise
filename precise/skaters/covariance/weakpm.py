from precise.skaters.covariance.weakfactory import weak_pcov_factory
from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r02_n100_t0, ewa_pm_emp_scov_r05_n50_t0


# Using partial moments...


def weak_pm_ewa_scov_r02_n100_t0(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_pm_emp_scov_r02_n100_t0, s=s, y=y, k=k, e=e)


def weak_pm_ewa_scov_r05_n50_t0(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_pm_emp_scov_r05_n50_t0, s=s, y=y, k=k, e=e)


WEAK_PM_DO_COV_SKATERS = [weak_pm_ewa_scov_r02_n100_t0, weak_pm_ewa_scov_r05_n50_t0 ]