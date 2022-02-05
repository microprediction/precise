import numpy as np
from precise.skaters.covarianceutil.covfunctions import try_invert, approx_diag_of_inv
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from typing import List
from itertools import zip_longest
from precise.skaters.locationutil.vectorfunctions import normalize

# Use only the diagonal elements of cov


def diagonal_portfolio_factory(pre=None, cov=None, sparse_approx=False, ridge=0.1):
    """ Min-var portfolio using only diagonal entries in cov
        (e.g. precision weighting of stacked models)
    :param pre:  precision matrix
    :param cov:  covariance matrix
    :param sparse_approx: Use fast approximate inversion of precision matrix
    :return:
    """
    if pre is not None:
        return diagonal_from_pre(pre=pre, sparse_approx=sparse_approx, ridge=ridge)
    else:
        return diagonal_from_cov(cov=cov, ridge=ridge)


def diagonal_from_pre(pre, sparse_approx=False, ridge=0.1):
    """ Signed min var portfolio summing to unity """
    if sparse_approx:
        cov = np.diag( approx_diag_of_inv(pre) )
    else:
        cov = try_invert(pre)
    return diagonal_from_cov(cov=cov, ridge=ridge)


def diagonal_from_cov(cov, ridge=0.1):
    mean_cov = np.mean(np.diag(cov))
    return normalize( [ 1/(d+ridge*mean_cov) for d in np.diag(cov)] )



