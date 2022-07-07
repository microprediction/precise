from precise.skaters.covarianceutil.covfunctions import try_invert, weaken_cov
from precise.skaters.portfoliostatic.unitportfactory import unitary_from_cov
from precise.skaters.portfolioutil.portfunctions import exclude_negative_weights, portfolio_variance
import scipy
from numpy.linalg import LinAlgError
import numpy as np
import math

# Fast long-only approximately min-var portfolios where the constraints are:
#       sum(w)=1,
#       w>0,
#       rel_entropish(w)<e

BIG_H = 1e10 # Relative entropish


def entropish(w):
    """ Etropish is a silly name for sum of log weights """
    if any([wi < 1e-8 for wi in w]):
        return -1.0e10
    else:
        return float(np.sum(np.log(w)))


def max_entropish(w):
    return entropish(np.ones_like(w)/len(w))


def rel_entropish(w):
    """ Always non-positive """
    return entropish(w) - max_entropish(w)


def ensure_rel_entropish(w, h:float):
    """ Crudely force portfolio to almost have rel_entropish > 1/h
    :param w:
    :param h:  h > 1
    :return:
    """
    if h<1:
        print(h)
        raise ValueError('Expecting h<1 got h='+str(h))

    if rel_entropish(w)>=-1/h:
        return w
    else:
        v = np.ones_like(w) / len(w)
        w_pos = exclude_negative_weights(w)
        while rel_entropish(v)>-1/h:
            v_prior = np.copy(v)
            v = 0.99*v + 0.01*np.array(w_pos)
        return v_prior



def weak_portfolio_factory(cov=None, pre=None, a=1.0, b=None, h=BIG_H, with_neg_mass=False):
    """ Long only portfolio somewhat similar to unitary min-var portfolio
        Uses a "weakenned" cov matrix

             sum(w)=1
             w>=0

    :param cov: Covariance matrix
    :param pre: Precision matrix (either cov or pre must be supplied)
    :param a:   Weakenning parameter
    :param b:   Weakenning parameter
    :param h:   Entropish paramters
    :param with_neg_mass:
    :return:
    """
    if cov is None:
        cov = try_invert(pre)
    w0 = unitary_from_cov(cov=cov)
    if b is not None:
        return _weak_known_params(cov=cov, a=a, b=b, w0=w0, with_neg_mass=with_neg_mass)
    else:
        return _weak_optimal_b(cov=cov, w0=w0, a=a, h=h, with_neg_mass=with_neg_mass)


def _weak_known_params(cov, a, b, w0, with_neg_mass=False):
    w1 = _weak_from_cov(cov=cov, a=a, b=b, w=w0, with_weak=False)
    return exclude_negative_weights(w1, with_neg_mass=with_neg_mass)


def optimal_b(cov, w0, a=1.0, h=BIG_H):

    def b_objective(u, w, a, v0, h):
        try:
            w1 = _weak_from_cov(cov, a=a, b=u, w=w, with_weak=False)
            w2 = exclude_negative_weights(ensure_rel_entropish(w1, h))
            v = portfolio_variance(cov=cov, w=w2) / v0
            return v
        except LinAlgError:
            bad_v = portfolio_variance(cov=cov, w=100 * w)
            return bad_v

    v0 = portfolio_variance(cov=cov, w=w0)
    vd = portfolio_variance(cov=np.diag(np.diag(cov)), w=np.ones_like(w0)/len(w0))
    initial_ratio = v0/vd
    if initial_ratio<1e-6:
        return 0.1
    else:
        res = scipy.optimize.minimize_scalar(fun=b_objective, bracket=(0.1,0.9), bounds=(0, 1), args=(w0, a, v0, h), method='Bounded')
        best_b = res.x
        if best_b<0:
            # Shouldn't happen but it does
            best_b = 0
        if best_b>1:
            # Ditto
            best_b = 1
        return best_b


def _weak_optimal_b(cov, w0, a, h=BIG_H, with_neg_mass=False, verbose=False):
    best_b = optimal_b(cov=cov, w0=w0, a=a, h=h)
    if verbose:
        print({'best_b':best_b})
    best_w = _weak_from_cov(cov=cov, a=1.0, b=best_b, w=w0, with_weak=False)
    return exclude_negative_weights(w=ensure_rel_entropish(best_w, h), with_neg_mass=with_neg_mass)


def _weak_from_cov(cov, w, a=1.0, b=0.75, with_weak=False):
    """
        Given long-short weights w, find different portfolio using weaker cov
        This is likely to have a lot less negative mass

        :param a  Diagnonal multipier for neg weights
        :param b  Additional multiplier for off-diag
    """
    d = [a if wi < 0.0 else 1.0 for wi in w]
    weak_cov = weaken_cov(cov=cov, diag_multipliers=d, off_diag_additional_factor=b)
    w1 = unitary_from_cov(weak_cov)
    return (w1, weak_cov) if with_weak else w1





