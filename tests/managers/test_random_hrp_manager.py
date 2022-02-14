import random
from precise.skaters.managerutil.managertesting import manager_test_run


def test_random_manager():
    from precise.skaters.managers.hrpmanagers import HRP_MANAGERS
    mgr = random.choice(HRP_MANAGERS)
    manager_test_run(mgr=mgr)


if __name__=='__main__':
    test_random_manager()