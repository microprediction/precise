import numpy as np
import pandas as pd
from precise.skaters.covarianceutil.covfunctions import to_symmetric, dense_weights_from_dict, normalize_dict_values, nearest_pos_def
from precise.skaters.covarianceutil.covfunctions import try_invert
from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from pypfopt import EfficientFrontier
from typing import List
from itertools import zip_longest
from precise.skaters.portfolioutil.portfunctions import var_scaled_returns
from pypfopt.exceptions import OptimizationError
from cvxpy.error import SolverError
try:
    from scipy.sparse.linalg import ArpackNoConvergence
except ImportError:
    from scipy.sparse.linalg.eigen import ArpackNoConvergence

from precise.skaters.covarianceutil.covfunctions import affine_shrink

# Thin wrapper for PyPortfolioOpt
# For full flexibility refer to the package https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html


PPO_METHODS = ['max_sharpe','min_volatility','max_quadratic_utility']
PPO_LONG_BOUNDS = (0, 1)
PPO_UNIT_BOUNDS = (-1, 1)


def ppo_sharpe_port(cov=None, pre=None, as_dense=True):
    """ Max Sharpe ratio portfolio using cov-implied returns
    :param cov:        Covariance matrix
    :param pre:        Precision matrix
    :param as_dense:   If false, will return weights in dict formet
    :return: np.array of weights
    """
    return ppo_portfolio_factory(method='max_sharpe', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_LONG_BOUNDS)


def ppo_vol_port(cov=None, pre=None, as_dense=True):
    return ppo_portfolio_factory(method='min_volatility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_LONG_BOUNDS)


def ppo_quad_port(cov=None, pre=None, as_dense=True):
    return ppo_portfolio_factory(method='max_quadratic_utility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_LONG_BOUNDS)


def ppo_sharpe_ls_port(cov=None, pre=None, as_dense=True):
    return ppo_portfolio_factory(method='max_sharpe', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_UNIT_BOUNDS)


def ppo_vol_ls_port(cov=None, pre=None, as_dense=True):
    return ppo_portfolio_factory(method='min_volatility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_UNIT_BOUNDS)


def ppo_quad_ls_port(cov=None, pre=None, as_dense=True):
    return ppo_portfolio_factory(method='max_quadratic_utility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_UNIT_BOUNDS)


def ppo_portfolio_factory(method:str, cov=None, pre=None, as_dense=False, weight_bounds=None,
                          risk_free_rate:float=0.02, mu:float=0.04, n_attempts=5, warn=False, throw=False):
    """
    :param method:
    :param cov:
    :param pre:
    :param as_dense:         If set to True, will force return of np.array even if supplied dataframe
    :param weight_bounds:
    :return:  Can return a dictionary of variable names and weights
    """

    expected_returns = var_scaled_returns(cov=cov,mu=mu,r=risk_free_rate)

    if weight_bounds is None:
        weight_bounds = PPO_LONG_BOUNDS

    if cov is None:
        cov = try_invert(pre)

    # Set return style
    as_series = (not as_dense) and isinstance(cov,pd.DataFrame)

    # Tidy up cov and send to optimizer ... repeatedly with more shrinkage as needed
    shrunk_cov = nearest_pos_def( to_symmetric( np.copy(cov) ) )
    converged = False
    warned = False
    for attempt_no in range(n_attempts):
        n_dim = np.shape(cov)[0]
        ef = EfficientFrontier(expected_returns=expected_returns, cov_matrix=shrunk_cov,
                               weight_bounds=weight_bounds)
        port_method = getattr(ef, method)
        try:
            if method=='max_sharpe':
                port_method(risk_free_rate=risk_free_rate)
            else:
                port_method()
            converged = True
        except (OptimizationError, SolverError, ArpackNoConvergence, UserWarning):
            converged = False
        if converged:
            break
        else:
            warned = True
            if warn:
                print('    warning: '+method+' did not converge on attempt '+str(attempt_no))
            shrunk_cov = affine_shrink(a=shrunk_cov,phi=1.02, lmbd=0.01, copy=False)

    if not converged:
        if throw:
            raise NotImplementedError('pyportfolio opt failed even after shrinkage')
        else:
            print('   PyPortfolioOpt failed ... falling back to minimum variance')
            from precise.skaters.portfoliostatic.equalport import equal_long_port
            return equal_long_port(cov=cov, as_dense=not as_series)

    if converged and warned:
        if warn:
            print('       ... but with shrinkage it converges okay.')

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
    w = ppo_portfolio_factory(method=method, pre=pre, cov=cov)
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
