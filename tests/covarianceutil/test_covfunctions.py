import numpy as np
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.covarianceutil.covfunctions import approx_diag_of_inv, cov_distance, seriation


def test_something():
    assert True


def test_cov_distance():
    cov = random_band_cov()
    d = cov_distance(cov=cov)


def test_seriation():
    cov = random_band_cov()
    l = seriation(cov=cov)
    print(l)



if __name__=='__main__':
    test_seriation()


