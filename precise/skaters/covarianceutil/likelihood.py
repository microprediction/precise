
import numpy as np
import math
import time


def scatter_likelihood(cov, pre, y, lb):
    """ Log likelihood of y
    :param cov:
    :param pre:
    :param y:      realized data points
    :param lb:     lower bound, returned if cov is degen
    :return:
    """
    # https://stats.stackexchange.com/questions/351549/maximum-likelihood-estimators-multivariate-gaussian
    p = len(y)
    (sign, abslogdet) = np.linalg.slogdet(cov)
    if np.isnan(abslogdet):
        ll = lb
    else:
        logdet = sign * abslogdet
        ll_term_1 = - (p / 2) * math.log(2 * math.pi)
        ll_term_2 = - (1 / 2) * logdet
        y_innovation = np.atleast_2d(y)
        y_innovation_t = y_innovation.transpose()
        ll_term_3 = - 1 / 2 * np.matmul(np.matmul(y_innovation, pre), y_innovation_t)[0, 0]
        ll = ll_term_1 + ll_term_2 + ll_term_3
    return ll


def cov_skater_loglikelihood(f, xs, n_burn=10, with_metrics=True, lb=-1000, ub=1000):
    """
        Gaussian likelihood of a cov skater applied to data xs

    :param f:
    :param lb, ub  lower and upper bounds for ll of individual point
    :param xs:
    :return:
    """
    start_time = time.time()
    inv_time = 0

    n_obs, n_dim = np.shape(xs)
    assert n_obs>n_burn
    s = {}


    for y in xs[:n_burn]:
        y_hat, y_cov, s = f(s=s,y=y,k=1)

    ll = 0
    y_hat_prev = None
    y_cov_prev = None
    for m,y in enumerate( xs[n_burn:]):
        if y_hat_prev is not None:
            # Evaluate last prediction
            inv_start_time = time.time()
            try:
                y_inv_prev = np.linalg.inv(y_cov_prev)
            except np.linalg.LinAlgError:
                y_inv_prev = np.linalg.pinv(y_cov_prev)
            inv_time += time.time()-inv_start_time

            dy = np.array(y) - np.array(y_hat_prev)
            ll_delta = scatter_likelihood(cov=y_cov_prev, pre=y_inv_prev, y=dy, lb=lb)
            if ll_delta>ub:
                ll_delta = ub
            ll += ll_delta

        # Store predictions for assessment against next data point
        y_hat_prev = y_hat
        y_cov_prev = y_cov

        # Make next prediction
        y_hat, y_cov, s = f(s=s, y=y, k=1)

    total_time = time.time()-start_time
    metrics = {'total time':total_time,'inversion time':inv_time,'time':total_time-inv_time}
    return ll, metrics if with_metrics else ll


if __name__=='__main__':
    from precise.skaters.covariance.runemp import run_emp_pcov_d0
    xs = np.random.randn(500,3)
    ll, metrics = cov_skater_loglikelihood(f=run_emp_pcov_d0, xs=xs, with_metrics=True)
    print(ll)
    from pprint import pprint
    pprint(metrics)






