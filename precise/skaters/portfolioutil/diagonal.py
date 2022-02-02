import numpy as np
from precise.skaters.covarianceutil.covfunctions import try_invert, approx_diag_of_inv
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from typing import List
from itertools import zip_longest
from precise.skaters.locationutil.vectorfunctions import normalize

# Use only the diagonal elements of cov


def prc_diag_port(pre=None, cov=None, sparse_approx=False):
    """ Min-var portfolio using only diagonal entries in cov
        (e.g. precision weighting of stacked models)
    :param pre:  precision matrix
    :param cov:  covariance matrix
    :param sparse_approx: Use fast approximate inversion of precision matrix
    :return:
    """
    if pre is not None:
        return diagonal_from_pre(pre=pre, sparse_approx=sparse_approx)
    else:
        return diagonal_from_cov(cov=cov)


def diagonal_from_pre(pre, sparse_approx=False):
    """ Signed min var portfolio summing to unity """
    if sparse_approx:
        cov = np.diag( approx_diag_of_inv(pre) )
    else:
        cov = try_invert(pre)
    return diagonal_from_cov(cov=cov)


def diagonal_from_cov(cov):
    return normalize( [1/d for d in np.diag(cov)] )


def diagonal_portfolio_variance(cov=None, pre=None):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = prc_diag_port(pre=pre, cov=cov)
    return portfolio_variance(cov=cov,w=w)


def prc_diag_alloc(covs:List, pres:List)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    # Remark: This was used in Marco Lopez de Prado's original HRP portfolio paper https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678
    return normalize([ 1/diagonal_portfolio_variance(cov=cov, pre=pre) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])




