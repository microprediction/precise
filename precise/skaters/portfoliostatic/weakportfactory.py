from precise.skaters.covarianceutil.covfunctions import try_invert, weaken_cov
from precise.skaters.portfoliostatic.unitportfactory import unitary_from_cov
from precise.skaters.portfolioutil.portfunctions import exclude_negative_weights, portfolio_variance
import scipy
from numpy.linalg import LinAlgError

# Fast long-only approximately min-var portfolios where the only constraints are sum(w)=1, w>0


def weak_portfolio_factory(cov=None, pre=None, a=1.0, b=None, with_neg_mass=False):
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
    w0 = unitary_from_cov(cov=cov)
    if b is not None:
        return _weak_known_params(cov=cov, a=a, b=b, w0=w0, with_neg_mass=with_neg_mass)
    else:
        return _weak_optimal_b(cov=cov, w0=w0, a=a, with_neg_mass=with_neg_mass)


def _weak_known_params(cov, a, b, w0, with_neg_mass=False):
    w1 = _weak_from_cov(cov=cov, a=a, b=b, w=w0, with_weak=False)
    return exclude_negative_weights(w1, with_neg_mass=with_neg_mass)


def optimal_b(cov, w0, a=1.0):
    def b_objective(u, w, a, v0):
        try:
            w1 = _weak_from_cov(cov, a=a, b=u[0], w=w, with_weak=False)
            v = portfolio_variance(cov=cov, w=exclude_negative_weights(w1)) / v0
            return v
        except LinAlgError:
            bad_v = portfolio_variance(cov=cov, w=100 * w)
            return bad_v

    v0 = portfolio_variance(cov=cov, w=w0)
    res = scipy.optimize.minimize(fun=b_objective, x0=0.75, bounds=[(0, 1)], args=(w0, a, v0))
    best_b = res.x[0]
    return best_b


def _weak_optimal_b(cov, w0, a, with_neg_mass=False):
    best_b = optimal_b(cov=cov, w0=w0, a=a)
    best_w = _weak_from_cov(cov=cov, a=1.0, b=best_b, w=w0, with_weak=False)
    return exclude_negative_weights(w=best_w,with_neg_mass=with_neg_mass)


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



