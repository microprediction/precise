from precise.skaters.managers.hrpmanagerfactory import hrp_weak_pm_manager_factory, hrp_weak_ewa_manager_factory


def herp_weak_pm_t0_d0_r025_n50_long_manager(y, s, k=1):
    assert k==1
    return hrp_weak_pm_manager_factory(y=y,s=s, target=0, r=0.025, n_emp=50)


def herp_weak_pm_t0_d0_r050_n25_long_manager(y, s, k=1):
    assert k==1
    return hrp_weak_pm_manager_factory(y=y,s=s, target=0, r=0.050, n_emp=25)


def herp_weak_emp_d0_r025_n50_long_manager(y, s, k=1):
    assert k==1
    return hrp_weak_ewa_manager_factory(y=y,s=s, r=0.025, n_emp=50)


def herp_weak_emp_d0_r050_n25_long_manager(y, s, k=1):
    assert k==1
    return hrp_weak_ewa_manager_factory(y=y,s=s, r=0.05, n_emp=25)




HRP_LONG_MANAGERS = [ herp_weak_pm_t0_d0_r025_n50_long_manager,
                      herp_weak_pm_t0_d0_r050_n25_long_manager,
                      herp_weak_emp_d0_r025_n50_long_manager,
                      herp_weak_emp_d0_r050_n25_long_manager
                      ]
HRP_LS_MANAGERS = []
HRP_MANAGERS = HRP_LONG_MANAGERS + HRP_LS_MANAGERS