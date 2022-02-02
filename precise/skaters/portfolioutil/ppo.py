import numpy as np
import pandas as pd
from precise.skaters.covarianceutil.covfunctions import to_symmetric, dense_weights_from_dict, normalize_dict_values, nearest_pos_def
from precise.skaters.covarianceutil.covfunctions import try_invert
from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from pypfopt import EfficientFrontier
from typing import List
from itertools import zip_longest

# Thin wrapper for some of the pyportfolio opt possibilities
# For full flexibility refer to the package https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html


PPO_METHODS = ['max_sharpe','min_volatility','max_quadratic_utility']


def ppo_sharpe_port(cov=None, pre=None, as_dense=True, weight_bounds=None):
    return _ppo_portfolio(method='max_sharpe', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=weight_bounds)


def ppo_vol_port(cov=None, pre=None, as_dense=True, weight_bounds=None):
    return _ppo_portfolio(method='min_volatility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=weight_bounds)


def ppo_quad_port(cov=None, pre=None, as_dense=True, weight_bounds=None):
    return _ppo_portfolio(method='max_quadratic_utility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=weight_bounds)


def _ppo_portfolio(method:str, cov=None, pre=None, as_dense=False, weight_bounds=None):
    """
    :param method:
    :param cov:
    :param pre:
    :param as_dense:         If set to True, will force return of np.array even if supplied dataframe
    :param weight_bounds:
    :return:  Can return a dictionary of variable names and weights
    """

    if weight_bounds is None:
        weight_bounds = (0,1)

    if cov is None:
        cov = try_invert(pre)

    # Set return style
    as_series = (not as_dense) and isinstance(cov,pd.DataFrame)

    # Tidy up cov and send to optimizer
    cov = to_symmetric(cov)
    cov = nearest_pos_def(cov)
    n_dim = np.shape(cov)[0]
    ef = EfficientFrontier(None, cov, weight_bounds=weight_bounds)
    port_method = getattr(ef, method)
    port_method()
    weights = ef.clean_weights()
    weights = normalize_dict_values(weights)

    if as_series:
        return pd.Series( index=list(weights.keys()), data=list(weights.values()) )
    else:
        return dense_weights_from_dict(weights, n_dim=n_dim)


def long_from_cov( cov, as_dense=True ):
    """ Backward compat """
    return ppo_vol_port(cov=cov, as_dense=as_dense)


def long_from_pre(pre, as_dense=True):
    """ Backward compate """
    return ppo_vol_port(pre=pre, as_dense=as_dense)


def ppo_portfolio_variance(method:str, cov=None, pre=None):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = _ppo_portfolio(method=method, pre=pre,cov=cov)
    return portfolio_variance(cov=cov,w=w)


def ppo_sharpe_alloc(covs:List, pres:List)->[float]:
    return _ppo_portfolio_allocation(method='max_sharpe', covs=covs, pres=pres)


def ppo_vol_alloc(covs:List, pres:List)->[float]:
    return _ppo_portfolio_allocation(method='min_volatility', covs=covs, pres=pres)


def ppo_quad_alloc(covs:List, pres:List)->[float]:
    return _ppo_portfolio_allocation(method='max_quadratic_utility', covs=covs, pres=pres)


def _ppo_portfolio_allocation(method:str, covs:List, pres:List)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    return normalize([ 1/ppo_portfolio_variance(method=method, cov=cov, pre=pre) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])
