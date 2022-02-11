from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from itertools import zip_longest
from typing import List
from precise.skaters.portfoliostatic.equalport import equal_long_port

def weak_portfolio_variance(cov=None, pre=None, **kwargs):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = weak_portfolio_factory(pre=pre, cov=cov, **kwargs)
    return portfolio_variance(cov=cov,w=w)


def weak_allocation_factory(covs:List, pres:List=None, **kwargs)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    if pres is None:
        pres = []
    try:
        w = normalize([ 1/weak_portfolio_variance(cov=cov, pre=pre, **kwargs) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])
    except RuntimeWarning:
        w = normalize([ 1.0 for _ in zip_longest(covs,pres)] )
    return w

