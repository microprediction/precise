
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfoliostatic.hrpport import hrp_unit_s5_port
import numpy as np


def test_parity():
    cov = random_band_cov()
    print(np.shape(cov))
    w = hrp_unit_s5_port(cov=cov)
    print(sum(w))