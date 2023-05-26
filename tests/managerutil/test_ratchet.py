from precise.skaters.managerutil.ratcheting import ratchet_trades
import numpy as np


def test_ratchet_trades_with_no_opportunity():
    w = [5/15, 5/15, 5/15]
    w_upper = [6/15, 6/15, 6/15]
    w_lower = [4/15, 4/15, 4/15]
    min_dw = 2
    expected_output = [0, 0, 0]
    assert ratchet_trades(w, w_lower, w_upper, min_dw) == expected_output


def test_ratchet_trades_with_opportunity():
    w       = [7/21, 7/21, 7/21]
    w_upper = [10/21, 6/21, 10/21]
    w_lower = [8/21,  4/21, 8/21]
    min_dw = 0.1
    dw = ratchet_trades(w, w_upper, w_lower, min_dw)
    assert dw[1]<0
    assert dw[2]>0


def test_ratchet_trades_with_mixed_opportunity():
    w       = [1/7, 3/7, 3/7]
    w_upper = [6/7, 6/7, 2/7]
    w_lower = [2/7, 4/7, 1/7]
    min_dw = 0.1
    dw = ratchet_trades(w, w_lower, w_upper, min_dw)
    assert dw[0]+dw[1]>0
    assert dw[2]<0


def test_random():
    w = sorted(np.random.rand(50))
    w = w/sum(w)
    w_ = np.random.rand(50)
    w_ = w_ / sum(w_)
    w_upper = 1.01*w_
    w_lower = 0.99*w_
    dw = ratchet_trades(w=w, w_lower=w_lower, w_upper=w_upper, min_dw=0.001)
    assert abs(sum(dw))<1e-6





if __name__=='__main__':
    test_random()
    test_ratchet_trades_with_mixed_opportunity()
    test_ratchet_trades_with_opportunity()
    test_ratchet_trades_with_no_opportunity()