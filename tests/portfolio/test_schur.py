
from precise.skaters.covarianceutil.covrandom import random_band_cov, random_factor_cov
from precise.skaters.portfoliostatic.schurport import SCHUR_PORT
import numpy as np


def test_schur():
    cov = random_band_cov(n=1000)
    cov = random_factor_cov(n=1000, n_dim=64)
    print(np.shape(cov))
    print(len(SCHUR_PORT))
    for port in SCHUR_PORT:
        print(port)
        w = port(cov=cov)
        assert len(w)==np.shape(cov)[0],' dim mismatch '


if __name__=='__main__':
    test_schur()