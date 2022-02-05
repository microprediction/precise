
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
import numpy as np


def test_parity():
    cov = random_band_cov()
    print(np.shape(cov))
    w = weak_portfolio_factory(cov=cov)
    assert len(w)==np.shape(cov)[0],' dim mismatch '


if __name__=='__main__':
    test_parity()