
import numpy as np
import math
import time


def cov_skater_loglikelihood(f, xs, n_burn=10, with_metrics=False):
    """
        Gaussian likelihood of a cov skater applied to data xs

    :param f:
    :param xs:
    :return:
    """
    start_time = time.time()
    inv_time = 0

    # https://stats.stackexchange.com/questions/351549/maximum-likelihood-estimators-multivariate-gaussian
    n_obs, n_dim = np.shape(xs)
    p = n_dim
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
            except:
                y_inv_prev = np.linalg.pinv(y_cov_prev)
            inv_time += time.time()-inv_start_time

            (sign, abslogdet) = np.linalg.slogdet(y_cov_prev)
            logdet = sign * abslogdet
            ll_term_1 = - p * math.log(2 * math.pi)
            ll_term_2 = - 1 / 2 * logdet
            y_innovation = np.atleast_2d(np.array(y)-np.array(y_hat_prev))
            y_innovation_t = y_innovation.transpose()
            ll_term_3 = - 1 / 2 * np.matmul( np.matmul( y_innovation_t, y_inv_prev), y_innovation )
            ll_delta = ll_term_1 + ll_term_2 + ll_term_3
            ll += ll_delta
        # Make next prediction
        y_hat, y_cov, s = f(s=s, y=y, k=1)

    total_time = time.time()-start_time
    metrics = {'total time':total_time,'inversion time':inv_time,'skater time':total_time-inv_time}
    return ll, metrics


if __name__=='__main__':
    from precise.skaters.covariance.empirical import emp_pcov_d0
    xs = np.random.randn(500,10)
    ll, metrics = cov_skater_loglikelihood(f=emp_pcov_d0, xs=xs, with_metrics=True)
    print(ll)
    from pprint import pprint
    pprint(metrics)






