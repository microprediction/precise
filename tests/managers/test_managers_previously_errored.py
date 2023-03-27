from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def test_troublesome_managers(return_w=False):
    if using_pyportfolioopt:
        from precise.skaters.managers.schurmanagers import schur_vol_vol_pm_t0_d0_r025_n50_s5_g100_long_manager as mgr2
        w2 = manager_test_run(mgr=mgr2)
        if return_w:
            return w


if __name__=='__main__':
    w = test_troublesome_managers(return_w=True)
    print(w)