import random
from precise.skaters.managerutil.managertesting import manager_test_run, manager_debug_run
from precise.skaters.managers.rpmanagers import rp_weak_pm_t0_p40_l21_long_manager as troublesome_mgr


def test_random_manager():
    from precise.skaters.managers.rpmanagers import RP_LONG_MANAGERS
    mgr = random.choice(RP_LONG_MANAGERS)
    j = random.choice([1, 5, 20])
    q = random.choice([1.0, 0.1])
    manager_test_run(mgr=mgr, j=j, q=q)


if __name__ == '__main__':
    manager_debug_run(troublesome_mgr)
    for _ in range(20):
        test_random_manager()
