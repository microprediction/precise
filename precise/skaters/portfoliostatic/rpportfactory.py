
import numpy as np
from precise.skaters.covarianceutil.covfunctions import try_invert
import riskparityportfolio as rp
from precise.skaters.portfolioutil.portfunctions import var_scaled_returns
import pandas as pd
from precise.skaters.covarianceutil.covfunctions import multiply_off_diag

# Thin wrapper for riskparityportfolio package


def rp_portfolio_factory(pre=None, cov=None, mu=0.02, risk_free_rate=0.02, phi=1.0):
    """ Signed min var portfolio summing to unity """

    if cov is None:
        cov = try_invert(pre)
    cov = multiply_off_diag(cov,phi=phi)
    expected_returns = var_scaled_returns(cov=cov,mu=mu,r=risk_free_rate)
    w = rp.vanilla.design(cov, b=expected_returns)
    return w




