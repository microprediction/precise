
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfolioutil.ppo import ppo_sharpe_port, ppo_quad_port, ppo_vol_port
import numpy as np


def test_ppo_sharpe():
    cov = random_band_cov()
    w = ppo_sharpe_port(cov=cov)
    assert len(w)==np.shape(cov)[0],' dim mismatch '


def test_ppo_quad():
    cov = random_band_cov()
    w = ppo_quad_port(cov=cov)
    assert len(w)==np.shape(cov)[0],' dim mismatch '


def test_ppo_vol():
    cov = random_band_cov()
    w = ppo_vol_port(cov=cov)
    assert len(w)==np.shape(cov)[0],' dim mismatch '



if __name__=='__main__':
    test_ppo_sharpe()
    test_ppo_quad()
    test_ppo_vol()