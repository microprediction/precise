import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run


def test_profile_schur_manager():
    from precise.skaters.managers.schurmanagers import schur_weak_weak_pm_t0_r025_n50_s25_g100_h150_long_manager as mgr
    j = random.choice([1, 5, 20])
    q = random.choice([1.0, 0.1])
    manager_test_run(mgr=mgr,j=j, q=q)
    print(mgr.__name__+' ran  okay')




if __name__=='__main__':
   test_profile_schur_manager()