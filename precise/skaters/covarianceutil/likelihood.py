
import numpy as np
import math
import time


def historical_log_likelihood(pre, xs, lb, mu=None):
    """ Log likelihood of matrix of data """
    from sklearn.covariance._empirical_covariance import log_likelihood, empirical_covariance
    if mu is None:
        emp_cov = empirical_covariance(xs)
    else:
        emp_cov = empirical_covariance(xs - mu)
    ll = log_likelihood(emp_cov=emp_cov, precision=pre)
    if ll<lb:
        ll=lb # Do something?!
    return ll


def vector_log_likelihood(pre, y, lb):
    """ Log likelihood of y
    :param cov:    Inverse of pre, the predicted precision
    :param pre:
    :param y:      realized data points
    :param lb:     lower bound, returned if cov is degen
    :return:
    """
    # c.f. sklearn
    #     term2 = 1/2 fast_logdet(pre)
    #     log_likelihood_  = -np.sum(emp_cov * precision) + fast_logdet(precision)
    #     log_likelihood_ -= p * np.log(2 * np.pi)
    # Derivation at
    # https://stats.stackexchange.com/questions/351549/maximum-likelihood-estimators-multivariate-gaussian
    from sklearn.utils.extmath import fast_logdet
    p = len(y)
    logdet = fast_logdet(pre)
    if logdet < lb:
        return lb
    else:
        ll_term_1 = - (p / 2) * math.log(2 * math.pi)
        ll_term_2 =  (1 / 2) * logdet
        y_innovation = np.atleast_2d(y)
        y_innovation_t = y_innovation.transpose()
        ll_term_3 = - 1 / 2 * np.matmul(np.matmul(y_innovation, pre), y_innovation_t)[0, 0]
        ll = ll_term_1 + ll_term_2 + ll_term_3
    return ll


def cov_likelihood(contestant, xs, n_burn=10, lb=-1000, ub=1000):
    # Used as evaluator
    return cov_skater_loglikelihood(f=contestant, xs=xs, with_metrics=True, n_burn=n_burn, lb=lb, ub=ub)


def cov_skater_loglikelihood(f, xs, n_burn=10, with_metrics=True, lb=-1000, ub=1000, verbose=True):
    """
        Gaussian likelihood of a cov skater applied to data xs

    :param f:  cov skater
    :param lb, ub  lower and upper bounds for ll of individual point
    :param xs:
    :return:
    """
    start_time = time.time()
    inv_time = 0

    n_obs, n_dim = np.shape(xs)
    assert n_obs>n_burn
    s = {}

    if verbose:
        print('   burn in for '+str(n_burn))
    for y in xs[:n_burn]:
        y_hat, y_cov, s = f(s=s, y=y, k=1, e=-1)

    if verbose:
        print('   evaluating  '+str(n_obs-n_burn))

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
            ll_delta = vector_log_likelihood(pre=y_inv_prev, y=dy, lb=lb)
            if ll_delta>ub:
                ll_delta = ub
            ll += ll_delta

        # Store predictions for assessment against next data point
        y_hat_prev = y_hat
        y_cov_prev = y_cov

        # Make next prediction
        y_hat, y_cov, s = f(s=s, y=y, k=1, e=1)

    total_time = time.time()-start_time
    metrics = {'total time':total_time,'inversion time':inv_time,'time':total_time-inv_time}
    return ll, metrics if with_metrics else ll


def pre_skater_loglikelihood(f, xs, n_burn=10, with_metrics=True, lb=-1000, ub=1000):
    """
        Gaussian likelihood of a precision skater applied to data xs

    :param f:
    :param lb, ub  lower and upper bounds for ll of individual point
    :param xs:
    :return:
    """
    start_time = time.time()

    n_obs, n_dim = np.shape(xs)
    assert n_obs>n_burn
    s = {}

    for y in xs[:n_burn]:
        y_hat, y_pre, s = f(s=s,y=y,k=1)

    ll = 0
    y_hat_prev = None
    y_pre_prev = None
    for m,y in enumerate( xs[n_burn:]):
        if y_hat_prev is not None:
            dy = np.array(y) - np.array(y_hat_prev)
            ll_delta = min( vector_log_likelihood(pre=y_pre_prev, y=dy, lb=lb),ub )
            ll += ll_delta

        # Store predictions for assessment against next data point
        y_hat_prev = y_hat
        y_pre_prev = y_pre

        # Make next prediction
        y_hat, y_pre, s = f(s=s, y=y, k=1)


    total_time = time.time()-start_time
    metrics = {'total time':total_time}
    return ll, metrics if with_metrics else ll



if __name__=='__main__':
    from precise.skaters.covariance.runemp import run_emp_pcov_d0
    xs = np.random.randn(500,3)
    ll, metrics = cov_skater_loglikelihood(f=run_emp_pcov_d0, xs=xs, with_metrics=True)
    print(ll)
    from pprint import pprint
    pprint(metrics)






