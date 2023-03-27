from precise.skaters.covarianceutil.covrandom import random_band_cov, random_factor_cov
from precise.skaters.portfoliostatic.schurport import schur_weak_weak_s5_g100_long_port as mgr
import numpy as np


def test_schur():
    cov = random_band_cov(n=1000)
    cov = random_factor_cov(n=1000, n_dim=25)
    schur_ports = [mgr]
    for port in schur_ports:
        print(port)
        w = port(cov=cov)
        assert len(w) == np.shape(cov)[0], ' dim mismatch '


if __name__ == '__main__':
    test_schur()
