from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from precise.skaters.portfoliostatic.ppoportfactory import ppo_vol_port
from typing import List
from itertools import zip_longest
from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.portfoliostatic.diagalloc import diagonal_allocation_factory


def vol_portfolio_variance(cov=None, pre=None):
    """
        Variance of the minimum volatility portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = ppo_vol_port(pre=pre, cov=cov)
    return portfolio_variance(cov=cov,w=w)


def vol_allocation_factory(covs:List, pres:List=None)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    if pres is None:
        pres = []
    try:
        return normalize([ 1/vol_portfolio_variance(cov=cov, pre=pre) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])
    except Exception as e:
        print('vol allocation failed')
        return diagonal_allocation_factory(covs=covs, pres=pres)


