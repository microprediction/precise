import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_debug_run


def test_random_schur_manager():
    from precise.skaters.managers.schurmanagers import schur_diag_weak_pm_t0_r050_n25_s5_g010_l21_long_manager as mgr
    j = random.choice([1, 5, 20])
    q = random.choice([1.0, 0.1])
    manager_debug_run(mgr=mgr,j=j, q=q, n_obs=500,n_dim=67)
    print(mgr.__name__+' ran  okay')



if __name__=='__main__':
    test_random_schur_manager()