import random
from precise.skaters.managerutil.managertesting import manager_test_run


def test_random_manager():
    from precise.skaters.managers.schurmanagers import SCHUR_MANAGERS
    mgr = random.choice(SCHUR_MANAGERS)
    manager_test_run(mgr=mgr)
    print(mgr.__name__+' ran  okay')


if __name__=='__main__':
    for _ in range(100):
        test_random_manager()