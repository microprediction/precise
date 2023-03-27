from precise.skaters.covarianceutil.covrandom import random_band_cov
import numpy as np
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def test_ppo_import():
    if using_pyportfolioopt:
        from precise.skaters.portfoliostatic.ppoportfactory import ppo_sharpe_port, ppo_quad_port, ppo_vol_port


def test_ppo_sharpe():
    if using_pyportfolioopt:
        from precise.skaters.portfoliostatic.ppoportfactory import ppo_sharpe_port
        cov = random_band_cov()
        w = ppo_sharpe_port(cov=cov)
        assert len(w) == np.shape(cov)[0], ' dim mismatch '


def test_ppo_quad():
    if using_pyportfolioopt:
        from precise.skaters.portfoliostatic.ppoportfactory import ppo_sharpe_port, ppo_quad_port
        cov = random_band_cov()
        w = ppo_quad_port(cov=cov)
        assert len(w) == np.shape(cov)[0], ' dim mismatch '


def test_ppo_quad():
    if using_pyportfolioopt:
        from precise.skaters.portfoliostatic.ppoportfactory import ppo_quad_port
        cov = random_band_cov()
        w = ppo_quad_port(cov=cov)
        assert len(w) == np.shape(cov)[0], ' dim mismatch '


if __name__ == '__main__':
    test_ppo_import()
    test_ppo_sharpe()
    test_ppo_quad()
