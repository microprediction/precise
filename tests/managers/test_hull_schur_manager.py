from precise.skatervaluation.managercomparisonutil.managertesting import manager_debug_run
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def dont_test_randomized_manager():
    if using_pyportfolioopt:
        from precise.skaters.managers.schurmanagers import schur_weak_vol_ewa_r001_n200_s50_g100_l20_long_manager as mgr
        j = 3
        q = 1.0
        manager_debug_run(mgr=mgr, j=j, q=q, n_dim=42, n_obs=2000)


if __name__=='__main__':
    dont_test_randomized_manager()