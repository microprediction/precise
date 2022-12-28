from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def test_vol_vol():
    if using_pyportfolioopt:
        from precise.skaters.managers.schurmanagers import schur_vol_vol_pm_t0_d0_r025_n50_s5_g100_long_manager as mgr
        manager_test_run(mgr=mgr, n_obs=20)



if __name__=='__main__':
    test_vol_vol()