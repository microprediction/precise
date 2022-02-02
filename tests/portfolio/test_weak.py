
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfolioutil.weak import prc_weak_port
import numpy as np


def test_parity():
    cov = random_band_cov()
    print(np.shape(cov))
    w = prc_weak_port(cov=cov)
    assert len(w)==np.shape(cov)[0],' dim mismatch '


if __name__=='__main__':
    test_parity()