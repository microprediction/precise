from precise.skaters.managers.schurmanagerfactory import schur_weak_weak_pm_manager_factory, \
    schur_weak_weak_ewa_manager_factory, schur_vol_vol_ewa_manager_factory, schur_weak_vol_ewa_manager_factory


# Some additional Hierarchical Risk-Parity managers that seem to do okay
# (i.e. Schur managers with gamma=delta=0)


def hrp_weak_weak_pm_t0_d0_r025_n50_s5_long_manager(y, s, k=1, e=1):
    assert k==1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, r=0.025, n_emp=50, n_split=5, e=e, gamma=0, delta=0)


def hrp_vol_vol_pm_t0_d0_r025_n50_s5_long_manager(y, s, k=1, e=1):
    assert k==1
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, r=0.025, n_emp=50, n_split=5, e=e, gamma=0, delta=0)


def hrp_vol_vol_pm_t0_d0_r025_n50_s50_long_manager(y, s, k=1, e=1):
    assert k==1
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, r=0.025, n_emp=50, n_split=50, e=e, gamma=0, delta=0)


def hrp_weak_vol_ewa_r025_n50_s50_long_manager(y, s, k=1, e=1):
    assert k==1
    return schur_weak_vol_ewa_manager_factory(y=y, s=s, r=0.025, n_emp=50, n_split=50, e=e, gamma=0, delta=0)




HRP_LONG_MANAGERS = [ hrp_weak_weak_pm_t0_d0_r025_n50_s5_long_manager,
                      hrp_vol_vol_pm_t0_d0_r025_n50_s5_long_manager,
                      hrp_vol_vol_pm_t0_d0_r025_n50_s50_long_manager,
                      hrp_weak_vol_ewa_r025_n50_s50_long_manager
                      ]
HRP_LS_MANAGERS = []
HRP_MANAGERS = HRP_LONG_MANAGERS + HRP_LS_MANAGERS