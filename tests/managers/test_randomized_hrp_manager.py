import random
from precise.skaters.managerutil.managertesting import manager_debug_run


def test_randomized_manager():
    from precise.skaters.managers.hrpmanagers import hrp_weak_vol_ewa_r001_n200_s50_l20_long_manager as mgr
    j = 20
    q = 1.0
    manager_debug_run(mgr=mgr, j=j, q=q, n_dim=500, n_obs=1000)


if __name__=='__main__':
    test_randomized_manager()