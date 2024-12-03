import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt
from precise.inclusion.riskparityportfolioinclusion import using_riskparityportfolio


def test_random_slurp_manager():
    from precise.skaters.managers.slurpmanagers import SLURP_LONG_MANAGERS
    if SLURP_LONG_MANAGERS:
        mgr = random.choice(SLURP_LONG_MANAGERS)
        j = random.choice([1, 5, 20])
        q = random.choice([1.0, 0.1])
        manager_test_run(mgr=mgr,j=j, q=q)
        print(mgr.__name__+' ran  okay')


def test_troublesome():
    if using_pyportfolioopt and using_riskparityportfolio:
        from precise.skaters.managers.slurpmanagers import slurp_vol_r001_s5_p20_g100_long_manger as mgr
        ys = random_cached_equity_dense(k=1, n_obs=50, n_dim=5, as_frame=False)
        s = {}
        for y in ys:
            w, s = mgr(y=y, s=s)


if __name__=='__main__':
    for _ in range(10):
        test_troublesome()
    for _ in range(100):
        test_random_slurp_manager()