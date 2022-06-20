import random
from precise.skaters.managerutil.managertesting import manager_test_run
from precise.skaters.managers.schurmanagers import schur_vol_vol_pm_t0_d0_r025_n50_s5_g100_long_manager


def test_vol_vol():
    manager_test_run(mgr=schur_vol_vol_pm_t0_d0_r025_n50_s5_g100_long_manager, n_obs=20)


if __name__=='__main__':
    test_vol_vol()