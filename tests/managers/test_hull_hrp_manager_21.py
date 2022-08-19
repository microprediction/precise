import random
from precise.skaters.managerutil.managertesting import manager_debug_run


def test_randomized_manager():
    from precise.skaters.managers.hrpmanagers import HRP_21_LONG_MANGERS
    mgr = random.choice(HRP_21_LONG_MANGERS)
    j = 3
    q = 1.0
    manager_debug_run(mgr=mgr, j=j, q=q, n_dim=42, n_obs=2000)


if __name__=='__main__':
    for _ in range(10):
        test_randomized_manager()