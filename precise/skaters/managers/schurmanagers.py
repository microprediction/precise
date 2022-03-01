from precise.skaters.managers.schurmanagerfactory import schur_weak_weak_pm_manager_factory, schur_weak_weak_ewa_manager_factory, \
    schur_diag_weak_pm_manager_factory, schur_vol_vol_ewa_manager_factory, schur_weak_vol_ewa_manager_factory, schur_diag_diag_ewa_manager_factory


def schur_weak_weak_pm_t0_r025_n50_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=1.0, delta=0.0)


def schur_weak_weak_pm_t0_r050_n25_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=1.0, delta=0.0)


def schur_weak_weak_ewa_r025_n50_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=1.0, delta=0.0)


def schur_weak_weak_ewa_r050_n25_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=1.0, delta=0.0)

#-#

def schur_weak_vol_ewa_r050_n25_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=1.0, delta=0.0)


def schur_vol_vol_ewa_r050_n25_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=1.0, delta=0.0)


def schur_diag_diag_ewa_r050_n25_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=1.0, delta=0.0)


def schur_diag_weak_pm_t0_r050_n25_s5_g100_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=1.0, delta=0.0)


SCHUR_GAMMA_100_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s5_g100_long_manager,
                                 schur_weak_weak_pm_t0_r050_n25_s5_g100_long_manager,
                                 schur_weak_weak_ewa_r025_n50_s5_g100_long_manager,
                                 schur_weak_weak_ewa_r050_n25_s5_g100_long_manager,
                                 schur_weak_vol_ewa_r050_n25_s5_g100_long_manager,
                                 schur_vol_vol_ewa_r050_n25_s5_g100_long_manager,
                                 schur_diag_diag_ewa_r050_n25_s5_g100_long_manager,
                                 schur_diag_weak_pm_t0_r050_n25_s5_g100_long_manager]


def schur_weak_weak_pm_t0_r025_n50_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.5, delta=0.0)


def schur_weak_weak_pm_t0_r050_n25_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=0.5, delta=0.0)


def schur_weak_weak_ewa_r025_n50_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=0.5, delta=0.0)


def schur_weak_weak_ewa_r050_n25_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=0.5, delta=0.0)

#-#

def schur_weak_vol_ewa_r050_n25_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.5, delta=0.0)


def schur_vol_vol_ewa_r050_n25_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.5, delta=0.0)


def schur_diag_diag_ewa_r050_n25_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.5, delta=0.0)


def schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.5, delta=0.0)




SCHUR_GAMMA_050_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s5_g050_long_manager,
                               schur_weak_weak_pm_t0_r050_n25_s5_g050_long_manager,
                               schur_weak_weak_ewa_r025_n50_s5_g050_long_manager,
                               schur_weak_weak_ewa_r050_n25_s5_g050_long_manager,
                               schur_weak_vol_ewa_r050_n25_s5_g050_long_manager,
                               schur_vol_vol_ewa_r050_n25_s5_g050_long_manager,
                               schur_diag_diag_ewa_r050_n25_s5_g050_long_manager,
                               schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager]



def schur_weak_weak_pm_t0_r025_n50_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50,gamma=0.1, delta=0.0)


def schur_weak_weak_pm_t0_r050_n25_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25,gamma=0.1, delta=0.0)


def schur_weak_weak_ewa_r025_n50_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50,gamma=0.1, delta=0.0)


def schur_weak_weak_ewa_r050_n25_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25,gamma=0.1, delta=0.0)

#-#

def schur_weak_vol_ewa_r050_n25_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5,gamma=0.1, delta=0.0)


def schur_vol_vol_ewa_r050_n25_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5,gamma=0.1, delta=0.0)


def schur_diag_diag_ewa_r050_n25_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5,gamma=0.1, delta=0.0)


def schur_diag_weak_pm_t0_r050_n25_s5_g010_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5,gamma=0.1, delta=0.0)




SCHUR_GAMMA_010_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s5_g010_long_manager,
                               schur_weak_weak_pm_t0_r050_n25_s5_g010_long_manager,
                               schur_weak_weak_ewa_r025_n50_s5_g010_long_manager,
                               schur_weak_weak_ewa_r050_n25_s5_g010_long_manager,
                               schur_weak_vol_ewa_r050_n25_s5_g010_long_manager,
                               schur_vol_vol_ewa_r050_n25_s5_g010_long_manager,
                               schur_diag_diag_ewa_r050_n25_s5_g010_long_manager,
                               schur_diag_weak_pm_t0_r050_n25_s5_g010_long_manager]




def schur_weak_weak_pm_t0_r025_n50_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50,gamma=0, delta=0.0)


def schur_weak_weak_pm_t0_r050_n25_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25,gamma=0, delta=0.0)


def schur_weak_weak_ewa_r025_n50_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50,gamma=0, delta=0.0)


def schur_weak_weak_ewa_r050_n25_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25,gamma=0, delta=0.0)

#-#

def schur_weak_vol_ewa_r050_n25_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5,gamma=0, delta=0.0)


def schur_vol_vol_ewa_r050_n25_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5,gamma=0, delta=0.0)


def schur_diag_diag_ewa_r050_n25_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5,gamma=0, delta=0.0)


def schur_diag_weak_pm_t0_r050_n25_s5_g000_long_manager(y, s, k=1,e=1):
    assert k==1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5,gamma=0, delta=0.0)




SCHUR_GAMMA_000_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s5_g000_long_manager,
                               schur_weak_weak_pm_t0_r050_n25_s5_g000_long_manager,
                               schur_weak_weak_ewa_r025_n50_s5_g000_long_manager,
                               schur_weak_weak_ewa_r050_n25_s5_g000_long_manager,
                               schur_weak_vol_ewa_r050_n25_s5_g000_long_manager,
                               schur_vol_vol_ewa_r050_n25_s5_g000_long_manager,
                               schur_diag_diag_ewa_r050_n25_s5_g000_long_manager,
                               schur_diag_weak_pm_t0_r050_n25_s5_g000_long_manager]



SCHUR_LONG_MANAGERS = SCHUR_GAMMA_100_LONG_MANAGERS + SCHUR_GAMMA_050_LONG_MANAGERS + SCHUR_GAMMA_010_LONG_MANAGERS + SCHUR_GAMMA_000_LONG_MANAGERS
SCHUR_LS_MANAGERS = []
SCHUR_MANAGERS = SCHUR_LONG_MANAGERS + SCHUR_LS_MANAGERS