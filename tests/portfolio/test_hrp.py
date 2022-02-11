
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfoliostatic.hrpportfactory import hrp_portfolio_factory
import numpy as np


def test_hrp():
    cov = random_band_cov()
    print(np.shape(cov))
    w = hrp_portfolio_factory(cov=cov)
    assert len(w)==np.shape(cov)[0],' dim mismatch '


if __name__=='__main__':
    test_hrp()