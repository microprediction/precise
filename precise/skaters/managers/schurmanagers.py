from precise.skaters.managers.schurmanagerfactory import schur_weak_pm_manager_factory, schur_weak_ewa_manager_factory


def schur_weak_pm_t0_d0_r025_n50_g100_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_pm_manager_factory(y=y, s=s, target=0, r=0.025, n_emp=50, gamma=1.0)


def schur_weak_pm_t0_d0_r050_n25_g100_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_pm_manager_factory(y=y, s=s, target=0, r=0.050, n_emp=25, gamma=1.0)


def schur_weak_emp_d0_r025_n50_g100_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_ewa_manager_factory(y=y, s=s, r=0.025, n_emp=50, gamma=1.0)


def schur_weak_emp_d0_r050_n25_g100_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_ewa_manager_factory(y=y, s=s, r=0.05, n_emp=25, gamma=1.0)


# gamma = 0.5

def schur_weak_pm_t0_d0_r025_n50_g050_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_pm_manager_factory(y=y, s=s, target=0, r=0.025, n_emp=50, gamma=0.5)


def schur_weak_pm_t0_d0_r050_n25_g050_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_pm_manager_factory(y=y, s=s, target=0, r=0.050, n_emp=25, gamma=0.5)


def schur_weak_emp_d0_r025_n50_g050_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_ewa_manager_factory(y=y, s=s, r=0.025, n_emp=50, gamma=0.5)


def schur_weak_emp_d0_r050_n25_g050_long_manager(y, s, k=1):
    assert k==1
    return schur_weak_ewa_manager_factory(y=y, s=s, r=0.05, n_emp=25, gamma=0.5)



SCHUR_100_LONG_MANAGERS = [ schur_weak_pm_t0_d0_r025_n50_g100_long_manager,
                      schur_weak_pm_t0_d0_r050_n25_g100_long_manager,
                      schur_weak_emp_d0_r025_n50_g100_long_manager,
                      schur_weak_emp_d0_r050_n25_g100_long_manager
                      ]
SCHUR_50_LONG_MANAGERS = [ schur_weak_pm_t0_d0_r025_n50_g050_long_manager,
                      schur_weak_pm_t0_d0_r050_n25_g050_long_manager,
                      schur_weak_emp_d0_r025_n50_g050_long_manager,
                      schur_weak_emp_d0_r050_n25_g050_long_manager
                      ]

SCHUR_LONG_MANAGERS = SCHUR_100_LONG_MANAGERS + SCHUR_50_LONG_MANAGERS
SCHUR_LS_MANAGERS = []
SCHUR_MANAGERS = SCHUR_LONG_MANAGERS + SCHUR_LS_MANAGERS