import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def test_random_manager(verbose=False, n_dim=7):
    if using_pyportfolioopt:
        from precise.skaters.managers.ppomanagers import PPO_LONG_MANAGERS
        mgr = random.choice(PPO_LONG_MANAGERS)
        print(mgr.__name__)
        manager_test_run(mgr=mgr, verbose=verbose, n_dim=n_dim)


if __name__=='__main__':
    for _ in range(50):
        test_random_manager(verbose=True, n_dim=500)