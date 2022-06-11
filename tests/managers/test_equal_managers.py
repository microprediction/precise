import random
from precise.skaters.managerutil.managertesting import manager_test_run
from precise.skaters.managers.equalmanagers import equal_daily_long_manager, equal_long_manager
from precise.skaters.managers.equalmanagers import equal_weekly_long_manager, equal_weekly_buy_and_hold_long_manager
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
from numpy.testing import assert_array_almost_equal




def test_random_manager():
    from precise.skaters.managers.allmanagers import LONG_MANAGERS
    mgr = random.choice(LONG_MANAGERS)
    manager_test_run(mgr=mgr)


def test_daily_equal():
    assert_equal_managing(equal_long_manager, equal_daily_long_manager)


def test_weekly_equal():
    assert_equal_managing(equal_weekly_long_manager, equal_weekly_buy_and_hold_long_manager)



def assert_equal_managing(mgr1,mgr2):
    ys = random_cached_equity_dense(k=1, n_obs=50, n_dim=3, as_frame=False)
    s1 = {}
    s2 = {}
    for y in ys:
        w1, s1 = mgr1(y=y, s=s1)
        w2, s2 = mgr2(y=y, s=s2)
        assert_array_almost_equal(w1,w2, err_msg='managers are not the same')



if __name__=='__main__':
    test_daily_equal()
    test_weekly_equal()