import random
from precise.skaters.managerutil.managertesting import manager_test_run
from precise.skatertools.data.equityhistorical import random_cached_equity_dense


def test_random_molyboga_manager():
    from precise.skaters.managers.molybogamanagers import MOLYBOGA_LONG_MANGERS
    mgr = random.choice(MOLYBOGA_LONG_MANGERS)
    j = random.choice([1, 5, 20])
    q = random.choice([1.0, 0.1])
    manager_test_run(mgr=mgr,j=j, q=q)
    print(mgr.__name__+' ran  okay')


def test_troublesome():
    from precise.skaters.managers.molybogamanagers import molyboga_r001_s5_gamma000_long_manger as mgr
    ys = random_cached_equity_dense(k=1, n_obs=50, n_dim=5, as_frame=False)
    s = {}
    for y in ys:
        w, s = mgr(y=y, s=s)


if __name__=='__main__':
    for _ in range(10):
        test_troublesome()
    for _ in range(100):
        test_random_molyboga_manager()