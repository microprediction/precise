import random
from precise.skaters.managerutil.managertesting import manager_test_run


def test_random_manager():
    from precise.skaters.managers.weakmanagers import WEAK_LONG_MANAGERS
    mgr = random.choice(WEAK_LONG_MANAGERS)
    manager_test_run(mgr=mgr)


if __name__=='__main__':
    for k in range(250):
        print(k)
        test_random_manager()