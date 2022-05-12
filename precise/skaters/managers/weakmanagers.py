from precise.skaters.managers.weakmanagerfactory import weak_pm_manager_factory, weak_ewa_manager_factory, weak_manager_factory
from precise.skaters.covariance.bufsk import buf_sk_glcv_pcov_d0_n100, buf_sk_glcv_pcov_d0_n100_t0, buf_sk_lw_pcov_d0_n100, buf_sk_mcd_pcov_d0_n100, buf_sk_lw_pcov_d1_n100
from precise.skaters.portfoliostatic.weakportfactory import BIG_H


def weak_pm_t0_d0_r025_n50_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.025, n_emp=50, e=e)


def weak_ewa_t0_d0_r025_n50_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.025, n_emp=50, e=e)


def weak_pm_t0_d0_r050_n50_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.050, n_emp=50, e=e)


def weak_ewa_t0_d0_r050_n50_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.050, n_emp=50, e=e)


# Weak with strong entropish constraint


def weak_pm_t0_d0_r025_n50_h125_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.025, n_emp=50, h=1.25, e=e)


def weak_ewa_t0_d0_r025_n50_h125_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.025, n_emp=50, h=1.25, e=e)


def weak_pm_t0_d0_r050_n50_h125_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.050, n_emp=50, h=1.25, e=e)


def weak_ewa_t0_d0_r050_n50_h125_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.050, n_emp=50, h=1.25, e=e)

# Weak with mild entropish constraint


def weak_pm_t0_d0_r025_n50_h500_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.025, n_emp=50, h=5, e=e)


def weak_ewa_t0_d0_r025_n50_h500_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.025, n_emp=50, h=5, e=e)


def weak_pm_t0_d0_r050_n50_h500_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.050, n_emp=50, h=5, e=e)


def weak_ewa_t0_d0_r050_n50_h500_long_manager(y, s, k=1, e=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.050, n_emp=50, h=5, e=e)



# Sklean


def weak_sk_lw_pcov_d0_n100_long_manager(y,s,k=1, e=1):
    return weak_manager_factory(y=y,s=s,f=buf_sk_lw_pcov_d0_n100, e=e)


def weak_sk_glcv_pcov_d0_n100_long_manager(y,s,k=1, e=1):
    return weak_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100, e=e)


def weak_sk_glcv_pcov_d0_n100_t0_long_manager(y,s,k=1, e=1):
    return weak_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100_t0, e=e)


def weak_sk_mcd_pcov_d0_n100_long_manager(y,s,k=1, e=1):
    return weak_manager_factory(y=y,s=s,f=buf_sk_mcd_pcov_d0_n100, e=e)


WEAK_LONG_MANAGERS = [weak_pm_t0_d0_r025_n50_long_manager,
                      weak_ewa_t0_d0_r025_n50_long_manager,
                      weak_pm_t0_d0_r050_n50_long_manager,
                      weak_ewa_t0_d0_r050_n50_long_manager,
                      weak_pm_t0_d0_r025_n50_h125_long_manager,
                      weak_ewa_t0_d0_r025_n50_h125_long_manager,
                      weak_pm_t0_d0_r050_n50_h125_long_manager,
                      weak_ewa_t0_d0_r050_n50_h500_long_manager,
                      weak_pm_t0_d0_r025_n50_h500_long_manager,
                      weak_ewa_t0_d0_r025_n50_h500_long_manager,
                      weak_pm_t0_d0_r050_n50_h500_long_manager,
                      weak_ewa_t0_d0_r050_n50_h500_long_manager,
                      weak_sk_lw_pcov_d0_n100_long_manager,
                      weak_sk_glcv_pcov_d0_n100_long_manager,
                      weak_sk_glcv_pcov_d0_n100_t0_long_manager,
                      weak_sk_mcd_pcov_d0_n100_long_manager
                      ]