from precise.skaters.covariance.ewapmfactory import ewa_pm_factory

# Partial moment skaters
# TODO: Make more autonomous
# Remark: Yes there are a few here and that's due to their initial success in Elo ratings.


def ewa_pm_emp_scov_r005_n100(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.005, n_emp=100)


def ewa_pm_emp_scov_r005_n100_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.005, n_emp=100, target=0)


def ewa_pm_emp_scov_r005_n200(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.005, n_emp=200)


def ewa_pm_emp_scov_r005_n200_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.005, n_emp=200, target=0)


def ewa_pm_emp_scov_r01_n100(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.01, n_emp=100)


def ewa_pm_emp_scov_r01_n100_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.01, n_emp=100, target=0)


def ewa_pm_emp_scov_r01_n200(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.01, n_emp=100)


def ewa_pm_emp_scov_r01_n200_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.01, n_emp=100, target=0)


def ewa_pm_emp_scov_r02_n50(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.02, n_emp=50)


def ewa_pm_emp_scov_r02_n50_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.02, n_emp=50, target=0)


def ewa_pm_emp_scov_r02_n100(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.02, n_emp=100)


def ewa_pm_emp_scov_r02_n100_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.02, n_emp=100, target=0)


def ewa_pm_emp_scov_r05_n50(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.05, n_emp=50)


def ewa_pm_emp_scov_r05_n50_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.05, n_emp=50, target=0)


def ewa_pm_emp_scov_r05_n25(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.02, n_emp=25)


def ewa_pm_emp_scov_r05_n25_t0(s, y, k=1, e=1):
    return ewa_pm_factory(s=s, y=y, k=k, r=0.02, n_emp=25, target=0)



EWA_PM_EMP_D0_COV_SKATERS_TM = [ewa_pm_emp_scov_r01_n100, ewa_pm_emp_scov_r01_n200,
                             ewa_pm_emp_scov_r02_n100, ewa_pm_emp_scov_r01_n200,
                             ewa_pm_emp_scov_r02_n50, ewa_pm_emp_scov_r02_n100,
                             ewa_pm_emp_scov_r05_n50, ewa_pm_emp_scov_r05_n25 ]

EWA_PM_EMP_D0_COV_SKATERS_T0 = [ewa_pm_emp_scov_r01_n100_t0, ewa_pm_emp_scov_r01_n200_t0,
                             ewa_pm_emp_scov_r02_n100_t0, ewa_pm_emp_scov_r01_n200_t0,
                             ewa_pm_emp_scov_r02_n50_t0, ewa_pm_emp_scov_r02_n100_t0,
                             ewa_pm_emp_scov_r05_n50_t0, ewa_pm_emp_scov_r05_n25_t0 ]


# some weak versions


EWA_PM_EMP_D0_COV_SKATERS = EWA_PM_EMP_D0_COV_SKATERS_TM + EWA_PM_EMP_D0_COV_SKATERS_T0

