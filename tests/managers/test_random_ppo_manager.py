import random
from precise.skaters.managerutil.managertesting import manager_test_run


def test_random_manager(verbose=False, n_dim=7):
    from precise.skaters.managers.ppomanagers import PPO_LONG_MANGERS
    mgr = random.choice(PPO_LONG_MANGERS)
    print(mgr.__name__)
    manager_test_run(mgr=mgr, verbose=verbose, n_dim=n_dim)


if __name__=='__main__':
    for _ in range(50):
        test_random_manager(verbose=True, n_dim=500)