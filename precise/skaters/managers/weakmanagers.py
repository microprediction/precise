from precise.skaters.managers.weakmanagerfactory import weak_pm_manager_factory, weak_ewa_manager_factory


def weak_pm_t0_d0_r025_n50_long_manager(y, s, k=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.025, n_emp=50)


def weak_ewa_t0_d0_r025_n50_long_manager(y, s, k=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.025, n_emp=50)


def weak_pm_t0_d0_r050_n50_long_manager(y, s, k=1):
    assert k==1
    return weak_pm_manager_factory(y=y,s=s, target=0, r=0.050, n_emp=50)


def weak_ewa_t0_d0_r050_n50_long_manager(y, s, k=1):
    assert k==1
    return weak_ewa_manager_factory(y=y,s=s, r=0.050, n_emp=50)


WEAK_LONG_MANAGERS = [weak_pm_t0_d0_r025_n50_long_manager,
                      weak_ewa_t0_d0_r025_n50_long_manager,
                      weak_pm_t0_d0_r050_n50_long_manager,
                      weak_ewa_t0_d0_r050_n50_long_manager]