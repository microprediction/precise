from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
from typing import List
from itertools import zip_longest
from precise.skaters.locationutil.vectorfunctions import normalize



def unitary_portfolio_variance(cov=None, pre=None, **kwargs):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = unit_portfolio_factory(pre=pre, cov=cov, **kwargs)
    return portfolio_variance(cov=cov,w=w)


def unitary_min_var_allocation_factory(covs:List, pres:List=None)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    if pres is None:
        pres = []
    return normalize([ 1/unitary_portfolio_variance(cov=cov, pre=pre) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])





