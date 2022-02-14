import random
from precise.skaters.managerutil.managertesting import manager_test_run


def test_random_manager():
    from precise.skaters.managers.ppomanagers import PPO_LONG_MANGERS
    mgr = random.choice(PPO_LONG_MANGERS)
    manager_test_run(mgr=mgr)


if __name__=='__main__':
    test_random_manager()