from precise.skaters.managers.schurmanagerfactory import schur_weak_weak_pm_manager_factory,\
    schur_weak_weak_ewa_manager_factory, schur_diag_weak_pm_manager_factory, \
    schur_diag_diag_ewa_manager_factory, schur_weak_diag_pm_manager_factory
    # gamma = 1.0
# r=0.025...
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def schur_weak_weak_pm_t0_r025_n50_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=1.0, delta=0.0, j=j,
                                              q=q)


def schur_weak_weak_pm_t0_r050_n25_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=1.0, delta=0.0, j=j,
                                              q=q)


def schur_weak_weak_ewa_r025_n50_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=1.0, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=1.0, delta=0.0, j=j, q=q)


# Same but with weak entropish and larger sub-portfolios

# ... first h=5.0
def schur_weak_weak_pm_t0_r025_n50_s25_g100_h500_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, h=5.0, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_pm_t0_r050_n25_s25_g100_h500_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, h=5.0, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_ewa_r025_n50_s25_g100_h500_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, h=5.0, gamma=1.0, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s25_g100_h500_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, h=5.0, gamma=1.0, delta=0.0, j=j, q=q)


SCHUR_GAMMA_100_S25_H500_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s25_g100_h500_long_manager,
                                          schur_weak_weak_pm_t0_r050_n25_s25_g100_h500_long_manager,
                                          schur_weak_weak_ewa_r025_n50_s25_g100_h500_long_manager,
                                          schur_weak_weak_ewa_r050_n25_s25_g100_h500_long_manager]


### Same but with weak entropish and larger sub-portfolios and s=100

# ... first h=5.0
def schur_weak_weak_pm_t0_r025_n50_s100_g100_h500_long_manager(y, s=100, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, h=5.0, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_pm_t0_r050_n25_s100_g100_h500_long_manager(y, s=100, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, h=5.0, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_ewa_r025_n50_s100_g100_h500_long_manager(y, s=100, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, h=5.0, gamma=1.0, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s100_g100_h500_long_manager(y, s=100, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, h=5.0, gamma=1.0, delta=0.0, j=j, q=q)


SCHUR_GAMMA_100_S100_H500_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s100_g100_h500_long_manager,
                                           schur_weak_weak_pm_t0_r050_n25_s100_g100_h500_long_manager,
                                           schur_weak_weak_ewa_r025_n50_s100_g100_h500_long_manager,
                                           schur_weak_weak_ewa_r050_n25_s100_g100_h500_long_manager]


# ... then h=1.5

def schur_weak_weak_pm_t0_r025_n50_s25_g100_h150_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, h=1.5, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_pm_t0_r050_n25_s25_g100_h150_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, h=1.0, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_ewa_r025_n50_s25_g100_h150_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, h=1.5, gamma=1.0, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s25_g100_h150_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, h=1.5, gamma=1.0, delta=0.0, j=j, q=q)


SCHUR_GAMMA_100_H150_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s25_g100_h150_long_manager,
                                      schur_weak_weak_pm_t0_r050_n25_s25_g100_h150_long_manager,
                                      schur_weak_weak_ewa_r025_n50_s25_g100_h150_long_manager,
                                      schur_weak_weak_ewa_r050_n25_s25_g100_h150_long_manager]


# ... then h=1.25

def schur_weak_weak_pm_t0_r025_n50_s25_g100_h125_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, h=1.25, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_pm_t0_r050_n25_s25_g100_h125_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, h=1.25, gamma=1.0, delta=0.0,
                                              j=j, q=q)


def schur_weak_weak_ewa_r025_n50_s25_g100_h125_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, h=1.25, gamma=1.0, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s25_g100_h125_long_manager(y, s=25, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, h=1.25, gamma=1.0, delta=0.0, j=j, q=q)


SCHUR_GAMMA_100_H125_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s25_g100_h125_long_manager,
                                      schur_weak_weak_pm_t0_r050_n25_s25_g100_h125_long_manager,
                                      schur_weak_weak_ewa_r025_n50_s25_g100_h125_long_manager,
                                      schur_weak_weak_ewa_r050_n25_s25_g100_h125_long_manager]


def schur_diag_diag_ewa_r050_n25_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=1.0, delta=0.0, j=j,
                                               q=q)


def schur_diag_weak_pm_t0_r050_n25_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=1.0,
                                              delta=0.0, j=j, q=q)


def schur_weak_diag_pm_t0_r050_n25_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_diag_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=1.0,
                                              delta=0.0, j=j, q=q)


# -#  r=0.05 ...

if using_pyportfolioopt:
    from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_pm_manager_factory
    from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_ewa_manager_factory, schur_weak_vol_ewa_manager_factory


    def schur_weak_vol_ewa_r050_n25_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=1.0, delta=0.0, j=j,
                                                  q=q)


    # Some close to HRP..

    def schur_weak_vol_ewa_r001_n200_s50_g100_l20_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_weak_vol_ewa_manager_factory(y=y, s=s, r=0.001, n_emp=200, n_split=50, e=e, gamma=100, delta=0, j=j,
                                                  q=q, l=20)


    def schur_weak_vol_ewa_r001_n200_s50_g100_l21_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_weak_vol_ewa_manager_factory(y=y, s=s, r=0.001, n_emp=200, n_split=50, e=e, gamma=100, delta=0, j=j,
                                                  q=q, l=21)

    def schur_vol_vol_ewa_r050_n25_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=1.0, delta=0.0, j=j, q=q)




    def schur_vol_vol_pm_t0_d0_r025_n50_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1, zeta=0):
        assert k == 1
        return schur_vol_vol_pm_manager_factory(y=y, s=s, n_emp=50, e=e, r=0.025, target=0, n_split=5, gamma=1.0, delta=0,
                                                zeta=zeta, j=j, q=q)


    def schur_vol_vol_pm_t0_d0_r025_n50_s25_g100_long_manager(y, s, k=1, e=1, j=1, q=1, zeta=0):
        assert k == 1
        return schur_vol_vol_pm_manager_factory(y=y, s=s, n_emp=50, e=e, r=0.025, target=0, n_split=25, gamma=1.0, delta=0,
                                                zeta=zeta, j=j, q=q)


    def schur_vol_vol_pm_t0_d0_r025_n50_s50_g100_long_manager(y, s, k=1, e=1, j=1, q=1, zeta=0):
        assert k == 1
        return schur_vol_vol_pm_manager_factory(y=y, s=s, n_emp=50, e=e, r=0.025, target=0, n_split=25, gamma=1.0, delta=0,
                                                zeta=zeta, j=j, q=q)


    SCHUR_GAMMA_100_VOL_VOL_LONG_MANAGERS = [schur_vol_vol_pm_t0_d0_r025_n50_s5_g100_long_manager,
                                         schur_vol_vol_pm_t0_d0_r025_n50_s25_g100_long_manager,
                                         schur_vol_vol_pm_t0_d0_r025_n50_s25_g100_long_manager,
                                         schur_vol_vol_pm_t0_d0_r025_n50_s50_g100_long_manager]
    SCHUR_GAMMA_100_WEAK_VOL_LONG_MANAGERS = [ schur_weak_vol_ewa_r050_n25_s5_g100_long_manager,
                                        schur_weak_vol_ewa_r001_n200_s50_g100_l20_long_manager,
                                        schur_weak_vol_ewa_r001_n200_s50_g100_l21_long_manager,
                                        schur_vol_vol_ewa_r050_n25_s5_g100_long_manager]
else:
    SCHUR_GAMMA_100_VOL_VOL_LONG_MANAGERS = []
    SCHUR_GAMMA_100_WEAK_VOL_LONG_MANAGERS = []

SCHUR_GAMMA_100_ENTROPISH_LONG_MANAGERS = SCHUR_GAMMA_100_H125_LONG_MANAGERS + \
                                          SCHUR_GAMMA_100_H150_LONG_MANAGERS + \
                                          SCHUR_GAMMA_100_S25_H500_LONG_MANAGERS + \
                                          SCHUR_GAMMA_100_S100_H500_LONG_MANAGERS

SCHUR_GAMMA_100_WEAK_WEAK_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s5_g100_long_manager,
                                           schur_weak_weak_pm_t0_r050_n25_s5_g100_long_manager,
                                           schur_weak_weak_ewa_r025_n50_s5_g100_long_manager,
                                           schur_weak_weak_ewa_r050_n25_s5_g100_long_manager]

SCHUR_GAMMA_100_DIAG_WEAK_LONG_MANAGERS = [schur_diag_weak_pm_t0_r050_n25_s5_g100_long_manager]

SCHUR_GAMMA_100_WEAK_DIAG_LONG_MANAGERS = [schur_weak_diag_pm_t0_r050_n25_s5_g100_long_manager]


SCHUR_GAMMA_100_DIAG_DIAG_LONG_MANAGERS = [schur_diag_diag_ewa_r050_n25_s5_g100_long_manager]


SCHUR_GAMMA_100_LONG_MANAGERS = SCHUR_GAMMA_100_ENTROPISH_LONG_MANAGERS + \
                                SCHUR_GAMMA_100_WEAK_WEAK_LONG_MANAGERS + \
                                SCHUR_GAMMA_100_VOL_VOL_LONG_MANAGERS + \
                                SCHUR_GAMMA_100_WEAK_VOL_LONG_MANAGERS + \
                                SCHUR_GAMMA_100_DIAG_WEAK_LONG_MANAGERS + \
                                SCHUR_GAMMA_100_DIAG_DIAG_LONG_MANAGERS +\
                                SCHUR_GAMMA_100_WEAK_DIAG_LONG_MANAGERS


# r=0.025...


def schur_weak_weak_pm_t0_r025_n50_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.5, delta=0.0, j=j,
                                              q=q)


def schur_weak_weak_pm_t0_r050_n25_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=0.5, delta=0.0, j=j,
                                              q=q)


def schur_weak_weak_ewa_r025_n50_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=0.5, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=0.5, delta=0.0, j=j, q=q)


# -# # r=0.05...


def schur_diag_diag_ewa_r050_n25_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.5, delta=0.0, j=j,
                                               q=q)


def schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.5,
                                              delta=0.0, j=j, q=q)

def schur_weak_diag_pm_t0_r050_n25_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_diag_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.5,
                                              delta=0.0, j=j, q=q)


SCHUR_GAMMA_050_LONG_MANAGERS_NOT_USING_PPO = [ schur_weak_weak_pm_t0_r025_n50_s5_g050_long_manager,
                                             schur_weak_weak_pm_t0_r050_n25_s5_g050_long_manager,
                                             schur_weak_weak_ewa_r025_n50_s5_g050_long_manager,
                                             schur_weak_weak_ewa_r050_n25_s5_g050_long_manager,
                                               schur_diag_diag_ewa_r050_n25_s5_g050_long_manager,
                                               schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager,
                                                schur_weak_diag_pm_t0_r050_n25_s5_g050_long_manager
                                               ]

if using_pyportfolioopt:
    from precise.skaters.managers.schurmanagerfactory import schur_weak_vol_ewa_manager_factory
    def schur_weak_vol_ewa_r050_n25_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.5, delta=0.0, j=j,
                                                  q=q)

    from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_ewa_manager_factory
    def schur_vol_vol_ewa_r050_n25_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.5, delta=0.0, j=j, q=q)

    SCHUR_GAMMA_050_LONG_MANAGERS_USING_PPO =  [schur_weak_vol_ewa_r050_n25_s5_g050_long_manager,
                                        schur_vol_vol_ewa_r050_n25_s5_g050_long_manager]
else:
    SCHUR_GAMMA_050_LONG_MANAGERS_USING_PPO = []


SCHUR_GAMMA_050_LONG_MANAGERS = SCHUR_GAMMA_050_LONG_MANAGERS_USING_PPO + \
                                SCHUR_GAMMA_050_LONG_MANAGERS_NOT_USING_PPO


def schur_weak_weak_pm_t0_r025_n50_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.0, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.1, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g020_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.2, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g030_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.3, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g040_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.4, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g050_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.5, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g060_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.6, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g070_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.7, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g080_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.8, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g090_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.9, delta=0.0, j=j,
                                              q=q, n_split=5)


def schur_weak_weak_pm_t0_r025_n50_s5_g100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=1.0, delta=0.0, j=j,
                                              q=q)


SCHUR_PM_S5_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s5_g000_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g010_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g020_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g030_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g040_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g050_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g060_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g070_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g080_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g090_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s5_g100_long_manager]


def schur_weak_weak_pm_t0_r025_n50_s2_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.0, delta=0.0, j=j,
                                              q=q, n_split=2)


def schur_weak_weak_pm_t0_r025_n50_s2_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.1, delta=0.0, j=j,
                                              q=q, n_split=2)


def schur_weak_weak_pm_t0_r025_n50_s2_g020_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.2, delta=0.0, j=j,
                                              q=q, n_split=2)


def schur_weak_weak_pm_t0_r025_n50_s2_g030_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.3, delta=0.0, j=j,
                                              q=q, n_split=2)


def schur_weak_weak_pm_t0_r025_n50_s2_g040_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0.4, delta=0.0, j=j,
                                              q=q, n_split=2)


SCHUR_PM_S2_LONG_MANAGERS = [schur_weak_weak_pm_t0_r025_n50_s2_g000_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s2_g010_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s2_g020_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s2_g030_long_manager,
                             schur_weak_weak_pm_t0_r025_n50_s2_g040_long_manager]



def schur_weak_weak_pm_t0_r050_n25_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=0.1, delta=0.0, j=j,
                                              q=q)


def schur_weak_weak_ewa_r025_n50_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=0.1, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=0.1, delta=0.0, j=j, q=q)


# -#


def schur_diag_diag_ewa_r050_n25_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.1, delta=0.0, j=j,
                                               q=q)


def schur_diag_weak_pm_t0_r050_n25_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.1,
                                              delta=0.0, j=j, q=q)


def schur_diag_weak_pm_t0_r050_n25_s5_g010_l21_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.5,
                                              delta=0.0, l=21, j=j, q=q)


def schur_diag_weak_pm_t0_r050_n25_s5_g010_l11_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.5,
                                              delta=0.0, l=11, j=j, q=q)


def schur_diag_weak_pm_t0_r050_n25_s5_g010_l7_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.5,
                                              delta=0.0, l=7, j=j, q=q)


def schur_weak_diag_pm_t0_r050_n25_s5_g010_l7_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_diag_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0.5,
                                              delta=0.0, l=7, j=j, q=q)


SCHUR_GAMMA_010_LONG_MANAGERS_NOT_USING_PPO = [schur_weak_weak_pm_t0_r025_n50_s5_g010_long_manager,
                                 schur_weak_weak_pm_t0_r050_n25_s5_g010_long_manager,
                                 schur_weak_weak_ewa_r025_n50_s5_g010_long_manager,
                                 schur_weak_weak_ewa_r050_n25_s5_g010_long_manager,
                                 schur_diag_diag_ewa_r050_n25_s5_g010_long_manager,
                                 schur_diag_weak_pm_t0_r050_n25_s5_g010_long_manager,
                                 schur_diag_weak_pm_t0_r050_n25_s5_g010_l11_long_manager,
                                 schur_diag_weak_pm_t0_r050_n25_s5_g010_l21_long_manager,
                                 schur_diag_weak_pm_t0_r050_n25_s5_g010_l7_long_manager,
                                 schur_weak_diag_pm_t0_r050_n25_s5_g010_l7_long_manager]

if using_pyportfolioopt:
    from precise.skaters.managers.schurmanagerfactory import schur_weak_vol_ewa_manager_factory
    def schur_weak_vol_ewa_r050_n25_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5,
                                                  gamma=0.1, delta=0.0, j=j,q=q)


    from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_ewa_manager_factory
    def schur_vol_vol_ewa_r050_n25_s5_g010_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0.1, delta=0.0, j=j, q=q)


    SCHUR_GAMMA_010_LONG_MANAGERS_USING_PPO =  [ schur_weak_vol_ewa_r050_n25_s5_g010_long_manager,
                                  schur_vol_vol_ewa_r050_n25_s5_g010_long_manager]
else:
    SCHUR_GAMMA_010_LONG_MANAGERS_USING_PPO = []


SCHUR_GAMMA_010_LONG_MANAGERS = SCHUR_GAMMA_010_LONG_MANAGERS_USING_PPO +\
                                SCHUR_GAMMA_010_LONG_MANAGERS_NOT_USING_PPO




def schur_weak_weak_pm_t0_r025_n50_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.025, n_emp=50, gamma=0, delta=0.0, j=j, q=q)


def schur_weak_weak_pm_t0_r050_n25_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_pm_manager_factory(y=y, s=s, target=0, e=e, r=0.050, n_emp=25, gamma=0, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r025_n50_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.025, n_emp=50, gamma=0, delta=0.0, j=j, q=q)


def schur_weak_weak_ewa_r050_n25_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_weak_weak_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, gamma=0, delta=0.0, j=j, q=q)


# -#


def schur_diag_diag_ewa_r050_n25_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0, delta=0.0, j=j, q=q)


def schur_diag_weak_pm_t0_r050_n25_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_weak_pm_manager_factory(y=y, s=s, e=e, r=0.05, target=0, n_emp=25, n_split=5, gamma=0, delta=0.0,
                                              j=j, q=q)

SCHUR_GAMMA_000_LONG_MANAGERS_NOT_USING_PPO = [schur_weak_weak_pm_t0_r025_n50_s5_g000_long_manager,
                                 schur_weak_weak_pm_t0_r050_n25_s5_g000_long_manager,
                                 schur_weak_weak_ewa_r025_n50_s5_g000_long_manager,
                                 schur_weak_weak_ewa_r050_n25_s5_g000_long_manager,
                                 schur_diag_diag_ewa_r050_n25_s5_g000_long_manager,
                                 schur_diag_weak_pm_t0_r050_n25_s5_g000_long_manager]

if using_pyportfolioopt:
    from precise.skaters.managers.schurmanagerfactory import schur_weak_vol_ewa_manager_factory
    def schur_weak_vol_ewa_r050_n25_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_weak_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0, delta=0.0, j=j, q=q)

    from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_ewa_manager_factory
    def schur_vol_vol_ewa_r050_n25_s5_g000_long_manager(y, s, k=1, e=1, j=1, q=1.0):
        assert k == 1
        return schur_vol_vol_ewa_manager_factory(y=y, s=s, e=e, r=0.05, n_emp=25, n_split=5, gamma=0, delta=0.0, j=j, q=q)

    SCHUR_GAMMA_000_LONG_MANAGERS_USING_PPO =  [schur_weak_vol_ewa_r050_n25_s5_g000_long_manager,
                                 schur_vol_vol_ewa_r050_n25_s5_g000_long_manager]
else:
    SCHUR_GAMMA_000_LONG_MANAGERS_USING_PPO = []

SCHUR_GAMMA_000_LONG_MANAGERS = SCHUR_GAMMA_000_LONG_MANAGERS_NOT_USING_PPO + \
                                SCHUR_GAMMA_000_LONG_MANAGERS_USING_PPO


SCHUR_J1_LONG_MANAGERS = SCHUR_GAMMA_100_LONG_MANAGERS + \
                         SCHUR_GAMMA_050_LONG_MANAGERS + \
                         SCHUR_GAMMA_010_LONG_MANAGERS + \
                         SCHUR_GAMMA_000_LONG_MANAGERS + \
                         SCHUR_PM_S5_LONG_MANAGERS + \
                         SCHUR_PM_S2_LONG_MANAGERS
SCHUR_LS_MANAGERS = []

SCHUR_LONG_MANAGERS = SCHUR_J1_LONG_MANAGERS

SCHUR_MANAGERS = SCHUR_LONG_MANAGERS + SCHUR_LS_MANAGERS
