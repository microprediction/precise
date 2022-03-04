from precise.skaters.covariance.avgfactory import avg_factory
from precise.skaters.covariance.weakewa import WEAK_EWA_DO_COV_SKATERS
from precise.skaters.covariance.weakpm import WEAK_PM_DO_COV_SKATERS, weak_pm_ewa_scov_r05_n50_t0


def weak_boot_ewa_pm(y,s,k=1,**ignore):
    fs = WEAK_PM_DO_COV_SKATERS + WEAK_EWA_DO_COV_SKATERS + WEAK_PM_DO_COV_SKATERS + WEAK_EWA_DO_COV_SKATERS
    return avg_factory(y=y,s=s,fs=fs, k=k, draw_probability=0.8)


def weak_boot_pm_ewa_scov_r05_n50_t0(y,s,k=1,**ignore):
    fs = [ weak_pm_ewa_scov_r05_n50_t0 ]*5
    return avg_factory(y=y,s=s,fs=fs, k=k, draw_probability=0.8)



WEAK_BOOT_D0_COV_SKATERS = [ weak_boot_ewa_pm, weak_boot_pm_ewa_scov_r05_n50_t0 ]

