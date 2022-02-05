from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from typing import List
from itertools import zip_longest
from precise.skaters.locationutil.vectorfunctions import normalize


def diagonal_portfolio_variance(cov=None, pre=None):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = diagonal_portfolio_factory(pre=pre, cov=cov)
    return portfolio_variance(cov=cov,w=w)


def diagonal_allocation_factory(covs:List, pres:List=None)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    if pres is None:
        pres = []
    # Remark: This was used in Marco Lopez de Prado's original HRP portfolio paper https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678
    return normalize([ 1/diagonal_portfolio_variance(cov=cov, pre=pre) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])


