import numpy as np
from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.portfolioutil.portfunctions import exclude_negative_weights, relative_negative_mass, portfolio_variance
import math

# Portfolios not requiring calls to optimizers


def unitary_from_pre(pre):
    """ Signed min var portfolio summing to unity """
    # No optimization required
    n_dim = np.shape(pre)[1]
    wones = np.ones(shape=(n_dim, 1))
    return normalize(np.squeeze(np.matmul(pre, wones)))


def unitary_from_cov(cov):
    try:
        pre = np.linalg.inv(cov)
    except:
        pre = np.linalg.pinv(cov)
    return unitary_from_pre(pre)


def try_invert(a):
    try:
        return np.linalg.inv(a)
    except:
        return np.linalg.pinv(a)
    return


def unitary_long_from_cov(cov, a=10, b=1.0, with_neg_mass=False):
    pre = try_invert(cov)
    return unitary_long_from_pre(pre, a=a, b=b, with_neg_mass=with_neg_mass)


def weaken_cov(cov, diag_multipliers:[float], off_diag_additional_factor=0.9):
    """  Augment a covariance matrix
    :param cov:
    :param diag_multipliers:             Vector to multiply diagonals by
    :param off_diag_additional_factor:   Additional multiplicative factor
    :return:
    """
    covs = np.copy(cov)
    for i, di in enumerate(diag_multipliers):
        covs[i, i] = covs[i, i] * di
        for j, dj in enumerate(diag_multipliers):
            if j != i:
                covs[i, j] = off_diag_additional_factor * math.sqrt(di * dj) * covs[i, j]
    return covs


def closer_to_long(cov, w, a=1.0, b=0.75):
    """
        Given long-short weights w, return new weights and augmented cov
        :param a  Diagnonal multipier for neg weights
        :param b  Additional multiplier for off-diag
    """
    d = [a if wi < 0.0 else 1.0 for wi in w]
    covs = weaken_cov(cov=cov, diag_multipliers=d, off_diag_additional_factor=b)
    return unitary_from_cov(covs), covs


def unitary_long_from_pre(pre, a=1.0, b=1.0, with_neg_mass=False ):
    w = unitary_from_pre(pre)
    cov = try_invert(pre)
    w1, augmented_cov = closer_to_long(cov, a, b, w)
    return exclude_negative_weights(w1, with_neg_mass=with_neg_mass)


def unitary_long_mininize(cov, with_neg_mass=False):
    """
    :param cov:
    :param with_neg_mass:
    :return:
    """

    def b_objective(u,w,v0):
        w1, augmented_cov = closer_to_long(cov, a=1, b=u[0], w=w)
        v = portfolio_variance(cov, exclude_negative_weights(w1))/v0
        return v

    import scipy
    w0 = unitary_from_cov(cov)
    v0 = portfolio_variance(cov,w0)
    res = scipy.optimize.minimize(fun=b_objective,x0=0.5, bounds=[(0,1)], args=(w0,v0))
    best_b = res.x[0]
    best_w, augmented_cov = closer_to_long(cov, a=1.0, b=best_b, w=w0)
    return exclude_negative_weights(best_w,with_neg_mass=with_neg_mass)







def unitary_long_gradual(cov, with_neg_mass=False):
    """ A rather speculative way to determine a long-only portfolio
    :param cov:
    :param with_neg_mass:
    :return:
    """
    a = 1.0
    b = 1.0
    aug_cov = np.copy(cov)
    w = unitary_from_cov(cov=cov)
    rnm = relative_negative_mass(w)
    baseline_var = portfolio_variance(cov, w)
    rel_var = 100000
    max_iter = 50
    for _ in range(max_iter):
        w_prev = np.copy(w)
        rel_var_prev = rel_var
        w, aug_cov = closer_to_long(cov=aug_cov, a=a, b=b, w=w)
        rnm = relative_negative_mass(w)
        rel_var = portfolio_variance(cov, exclude_negative_weights(w))/baseline_var
        b = b*0.975
        if (rnm<0.005):
            break
        if rel_var>=1.01*rel_var_prev:
            break

    if rel_var_prev<rel_var:
        w = w_prev
    return exclude_negative_weights(w,with_neg_mass=with_neg_mass)






