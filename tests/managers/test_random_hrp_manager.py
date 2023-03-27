import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run


def test_random_manager():
    from precise.skaters.managers.hrpmanagers import HRP_MANAGERS
    mgr = random.choice(HRP_MANAGERS)
    j = random.choice([1, 5, 20])
    q = random.choice([1.0, 0.1])
    manager_test_run(mgr=mgr, j=j, q=q)


if __name__ == '__main__':
    for _ in range(20):
        test_random_manager()
