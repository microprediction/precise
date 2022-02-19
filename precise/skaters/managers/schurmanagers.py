from precise.skaters.managers.schurmanagerfactory import schur_weak_weak_pm_manager_factory, schur_weak_weak_ewa_manager_factory, schur_diag_weak_pm_manager_factory


def schur_weak_pm_t0_d0_r025_n50_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=1.0)


def schur_weak_pm_t0_d0_r050_n25_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=1.0)


def schur_weak_emp_d0_r025_n50_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=1.0)


def schur_weak_emp_d0_r050_n25_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=1.0)


# gamma = 0.5

def schur_weak_pm_t0_d0_r025_n50_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.5)


def schur_weak_pm_t0_d0_r050_n25_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=0.5)



def schur_weak_emp_d0_r025_n50_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=0.5)


def schur_weak_emp_d0_r050_n25_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=0.5)


# gamma = 0.25


def schur_weak_pm_t0_d0_r050_n25_g025_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=0.25)


def schur_weak_emp_d0_r025_n50_g025_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=0.25)


# diagonal allocation


def schur_diag_weak_pm_t0_d0_r025_n50_g050_long_manager(y, s, k=1, e=1):
    assert k==1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.025,  target=0,n_emp=50, gamma=0.50)


def schur_diag_weak_pm_t0_d0_r025_n50_g025_long_manager(y, s, k=1, e=1):
    assert k==1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.025,  target=0, n_emp=50, gamma=0.25)


SCHUR_WEAK_WEAK_100_LONG_MANAGERS = [schur_weak_pm_t0_d0_r025_n50_g100_long_manager,
                                     schur_weak_pm_t0_d0_r050_n25_g100_long_manager,
                                     schur_weak_emp_d0_r025_n50_g100_long_manager,
                                     schur_weak_emp_d0_r050_n25_g100_long_manager
                                     ]
SCHUR_WEAK_WEAK_50_LONG_MANAGERS = [schur_weak_pm_t0_d0_r025_n50_g050_long_manager,
                                    schur_weak_pm_t0_d0_r050_n25_g050_long_manager,
                                    schur_weak_emp_d0_r025_n50_g050_long_manager,
                                    schur_weak_emp_d0_r050_n25_g050_long_manager
                                    ]

SCHUR_WEAK_WEAK_25_LONG_MANAGERS = [schur_weak_pm_t0_d0_r050_n25_g025_long_manager,
                                    schur_weak_emp_d0_r025_n50_g025_long_manager
                                    ]

SCHUR_DIAG_WEAK_LONG_MANAGERS = [schur_diag_weak_pm_t0_d0_r025_n50_g025_long_manager,
                                 schur_diag_weak_pm_t0_d0_r025_n50_g050_long_manager
                                 ]



SCHUR_LONG_MANAGERS = SCHUR_WEAK_WEAK_100_LONG_MANAGERS + SCHUR_WEAK_WEAK_50_LONG_MANAGERS + \
                      SCHUR_WEAK_WEAK_25_LONG_MANAGERS  + SCHUR_DIAG_WEAK_LONG_MANAGERS
SCHUR_LS_MANAGERS = []
SCHUR_MANAGERS = SCHUR_LONG_MANAGERS + SCHUR_LS_MANAGERS