import numpy as np
from precise.skaters.covarianceutil.covfunctions import try_invert
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from typing import List
from itertools import zip_longest
from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.covarianceutil.covfunctions import multiply_off_diag

# Long-short min-var portfolios where the only constraint is sum(w)=1


def unit_portfolio_factory(pre=None, cov=None, phi=1.0):
    """ Signed min var portfolio summing to unity """
    if (pre is not None):
        if (phi>1.0-1e-4):
            return unitary_from_pre(pre=pre, phi=phi)
        else:
            cov = try_invert(pre)
            return unitary_from_cov(cov=cov, phi=phi)
    else:
        return unitary_from_cov(cov=cov, phi=phi)


def unitary_from_pre(pre, phi=1.0):
    """ Signed min var portfolio summing to unity """
    # No optimization required
    n_dim = np.shape(pre)[1]
    wones = np.ones(shape=(n_dim, 1))
    w = normalize(np.squeeze(np.matmul(pre, wones)))
    sum_w = np.sum(w)
    if abs(sum_w-1)<1e-4:
        return np.array(w)
    else:
        print('Warning. Unitary portfolio failed.')
        return np.ones_like(w)/n_dim


def unitary_from_cov(cov,phi=1.0):
    cov = multiply_off_diag(cov, phi=phi)
    pre = try_invert(cov)
    return unitary_from_pre(pre=pre)


def unitary_portfolio_variance(cov=None, pre=None):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = unit_portfolio_factory(pre=pre, cov=cov)
    return portfolio_variance(cov=cov,w=w)


def prc_unit_alloc(covs:List, pres:List=None)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariancecomparisonutil matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    if pres is None:
        pres = []
    return normalize([ 1/unitary_portfolio_variance(cov=cov, pre=pre) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])


