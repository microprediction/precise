import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run
from precise.skaters.managers.equalmanagers import equal_long_manager
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
from numpy.testing import assert_array_almost_equal


def test_random_manager():
    from precise.skaters.managers.allmanagers import LONG_MANAGERS
    mgr = random.choice(LONG_MANAGERS)
    manager_test_run(mgr=mgr)


def test_daily_equal():
    assert_equal_managing(equal_long_manager, equal_long_manager, j=1, q=1)


def test_smoothing_equal():
    assert_equal_managing(equal_long_manager, equal_long_manager, j=1, q=0.5)


def test_weekly_equal():
    assert_equal_managing(equal_long_manager, equal_long_manager, j=5, q=1)


def test_weekly_smoothing_equal():
    assert_equal_managing(equal_long_manager, equal_long_manager, j=5, q=0.5)


def test_random_j_q_equal():
    j = random.choice([1,5,20])
    q = random.choice([1,0,0.1])
    assert_equal_managing(equal_long_manager, equal_long_manager, j=j, q=q)


def assert_equal_managing(mgr1,mgr2, j, q):
    ys = random_cached_equity_dense(k=1, n_obs=50, n_dim=3, as_frame=False)
    s1 = {}
    s2 = {}
    for y in ys:
        w1, s1 = mgr1(y=y, s=s1, j=j, q=q)
        w2, s2 = mgr2(y=y, s=s2, j=j, q=q)
        assert_array_almost_equal(w1,w2, err_msg='equal / equality managers are not the same with j='+str(j)+' and q='+str(q))



if __name__=='__main__':
    for _ in range(10):
        test_daily_equal()
        test_weekly_equal()
        test_smoothing_equal()
        test_weekly_smoothing_equal()
        test_random_j_q_equal()
        print('yeh')