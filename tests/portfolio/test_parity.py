
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfolioutil.parity import prc_hrp_diag_5
import numpy as np


def test_parity():
    cov = random_band_cov()
    print(np.shape(cov))
    w = prc_hrp_diag_5(cov=cov)
    print(sum(w))