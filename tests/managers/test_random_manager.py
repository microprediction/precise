import random
from precise.skaters.managerutil.managertesting import manager_test_run
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
from numpy.testing import assert_array_almost_equal
import numpy as np


def assert_manager_does_not_alter_y(mgr):
    ys = random_cached_equity_dense(k=1, n_obs=50, n_dim=5, as_frame=False)
    s = {}
    for y in ys:
        y_prev = [ yi for yi in y ]
        w, s = mgr(y=y, s=s)
        assert_array_almost_equal(np.array(y_prev), np.array(y), err_msg='manager '+str(mgr.__name__)+' alters y')


def test_random_manager():
    from precise.skaters.managers.allmanagers import LONG_MANAGERS
    mgr = random.choice(LONG_MANAGERS)
    print('Testing '+mgr.__name__)
    assert_manager_does_not_alter_y(mgr=mgr)
    j = random.choice([1,5,20])
    manager_test_run(mgr=mgr,j=j)


if __name__=='__main__':
    for _ in range(250):
        test_random_manager()