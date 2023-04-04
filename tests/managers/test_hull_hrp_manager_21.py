import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_debug_run
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def dont_test_randomized_manager():
    if using_pyportfolioopt:
        from precise.skaters.managers.hrpmanagers import HRP_21_LONG_MANGERS_USING_PPO
        mgr = random.choice(HRP_21_LONG_MANGERS_USING_PPO)
        j = 3
        q = 1.0
        manager_debug_run(mgr=mgr, j=j, q=q, n_dim=42, n_obs=2000)


if __name__=='__main__':
    for _ in range(10):
        dont_test_randomized_manager()