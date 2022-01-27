from precise.skaters.covariance.ewapmfactory import partial_ema_scov_factory


def ewa_pm_emp_scov_r005(s, y, k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.005)


def ewa_pm_emp_scov_r01(s, y, k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.01)


def ewa_pm_emp_scov_r02(s, y, k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.02,n_emp=100)


def ewa_pm_emp_scov_r05(s, y, k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.05,n_emp=100)



def ewa_pm_emp_scov_r005_t0(s, y, k=1):
     """ target = 0 """
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.005, target=0)


def ewa_pm_emp_scov_r01_t0(s, y, k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.01, target=0)


def ewa_pm_emp_scov_r02_t0(s, y, k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.02, target=0,n_emp=100)


def ewa_pm_emp_scov_r05_t0(s, y, k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.05, target=0,n_emp=100)


EWA_PM_EMP_D0_COV_SKATERS = [ewa_pm_emp_scov_r005, ewa_pm_emp_scov_r01, ewa_pm_emp_scov_r02, ewa_pm_emp_scov_r05,
                             ewa_pm_emp_scov_r005_t0, ewa_pm_emp_scov_r01_t0, ewa_pm_emp_scov_r02_t0, ewa_pm_emp_scov_r05_t0]
