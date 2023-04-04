from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
import numpy as np
from precise.skaters.covarianceutil.covfunctions import nearest_pos_def, is_positive_def


def test_weak():
    cov = random_band_cov()
    print(np.shape(cov))
    w = weak_portfolio_factory(cov=cov)
    assert all([wi >= 0 for wi in w]), ' weak portfolio was not long only'
    assert len(w) == np.shape(cov)[0], ' dim mismatch '


def test_weak_entropish():
    cov = random_band_cov()
    print(np.shape(cov))
    w = weak_portfolio_factory(cov=cov, h=2)
    assert all([wi >= 0 for wi in w]), ' weak portfolio was not long only'


def test_weak_entropish_again():
    cov = random_band_cov(n_dim=5)
    print(np.shape(cov))
    w = weak_portfolio_factory(cov=cov, h=5.0)
    assert len(w) == np.shape(cov)[0], ' dim mismatch '
    contrib = w * np.dot(cov, w)
    print(contrib)
    w_eq = np.ones_like(w) / len(w)
    contrib_eq = w_eq * np.dot(cov, w_eq)
    print(contrib_eq)


if __name__ == '__main__':
    test_weak_entropish_again()
