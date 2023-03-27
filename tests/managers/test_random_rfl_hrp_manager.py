import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run


def test_random_manager(return_w=False):
    from precise.skaters.managers.rflmanagers import RFL_LONG_MANAGERS
    if RFL_LONG_MANAGERS:
        mgr = random.choice(RFL_LONG_MANAGERS)
        w = manager_test_run(mgr=mgr)
        if return_w:
            return w


if __name__=='__main__':
    for _ in range(50):
        w = test_random_manager(return_w=True)
        print(w)