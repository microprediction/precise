from precise.skaters.covarianceutil.covfunctions import try_invert, weaken_cov
from precise.skaters.portfolioutil.unitary import weak_from_cov
from precise.skaters.portfolioutil.portfunctions import exclude_negative_weights, portfolio_variance
from precise.skaters.locationutil.vectorfunctions import normalize
from itertools import zip_longest
import scipy
from typing import List

# Fast long-only approximately min-var portfolios where the only constraints are sum(w)=1, w>0


def prc_weak_port(cov=None, pre=None, a=1.0, b=None, with_neg_mass=False):
    """ Long only portfolio somewhat similar to unitary min-var portfolio
        Uses a "weakenned" cov matrix

             sum(w)=1
             w>=0

    :param cov: Covariance matrix
    :param pre: Precision matrix (either cov or pre must be supplied)
    :param a:   Weakenning parameter
    :param b:   Weakenning parameter
    :param with_neg_mass:
    :return:
    """
    if cov is None:
        cov = try_invert(pre)
    w0 = weak_from_cov(cov=cov)
    if b is not None:
        return weak_known_params(cov=cov, a=a, b=b, w0=w0, with_neg_mass=with_neg_mass)
    else:
        return weak_optimal_b(cov=cov, w0=w0, a=a, with_neg_mass=with_neg_mass)


def weak_portfolio_from_cov(cov, w, a=1.0, b=0.75, with_weak=False):
    """
        Given long-short weights w, find different portfolio using weaker cov
        This is likely to have a lot less negative mass

        :param a  Diagnonal multipier for neg weights
        :param b  Additional multiplier for off-diag
    """
    d = [a if wi < 0.0 else 1.0 for wi in w]
    weak_cov = weaken_cov(cov=cov, diag_multipliers=d, off_diag_additional_factor=b)
    w1 = weak_from_cov(weak_cov)
    return w1, weak_cov if with_weak else w1


def weak_known_params(cov, a, b, w0, with_neg_mass=False):
    w1 = weak_portfolio_from_cov(cov, a=a, b=b, w=w0)
    return exclude_negative_weights(w1, with_neg_mass=with_neg_mass)


def weak_optimal_b(cov, w0, a, with_neg_mass=False):

    def b_objective(u,w,a, v0):
        w1 = weak_portfolio_from_cov(cov, a=a, b=u[0], w=w, with_weak=False)
        v = portfolio_variance(cov, exclude_negative_weights(w1))/v0
        return v

    v0 = portfolio_variance(cov,w0)
    res = scipy.optimize.minimize(fun=b_objective,x0=0.75, bounds=[(0,1)], args=(w0, a, v0))
    best_b = res.x[0]
    best_w, augmented_cov = weak_portfolio_from_cov(cov, a=1.0, b=best_b, w=w0)
    return exclude_negative_weights(best_w,with_neg_mass=with_neg_mass)


def weak_portfolio_variance(cov=None, pre=None, **kwargs):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = prc_weak_port(pre=pre, cov=cov, **kwargs)
    return portfolio_variance(cov=cov,w=w)


def prc_weak_alloc(covs:List, pres:List, **kwargs)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    return normalize([ 1/weak_portfolio_variance(cov=cov, pre=pre, **kwargs) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])

