from precise.skaters.covarianceutil.conventions import is_data, infer_dimension, X_TYPE, X_DATA_TYPE
from precise.skaters.vector.bufferstatspre import buf_mean_and_median
from precise.skaters.vector.movingaveragepre import sma
import numpy as np
from precise.skaters.vectorutil.hubermean import huber_deriv, parallel_bisection_root_finder, mean_huber_squared_error
from pprint import pprint


# Pre-skaters based on generalized Huber metric


def huber_pcov(s:dict,x:X_TYPE=None, n_dim=None, n_buffer=100, n_iter=20, atol=1e-8, r=0.05, a=1.0, b=1.0)->dict:
    """ Running Huber covariance estimate
    :param s:
    :param x:
    :return:
    """
    if not s:
        s = _huber_pcov_init(s=s,x=x,n_dim=n_dim, n_buffer=n_buffer)
    if is_data(x):
        s = _huber_pcov_update(s=s,x=x,n_buffer=n_buffer, n_iter=n_iter, atol=atol, r=r,a=a, b=b )
    return s


def _huber_pcov_init(s:dict=None, x:X_TYPE=None, n_dim:int=None, n_buffer:int=None):
    n_dim = infer_dimension(x=x, n_dim=n_dim)
    if not s:
        s = dict()
    s.update( {'buf':{},
               'sma':{},
               'pcov': np.zeros(shape=(n_dim,n_dim)),
               'n_buffer':n_buffer} )
    return s


def _huber_pcov_update(s:dict, x:X_DATA_TYPE,n_buffer, n_iter=10, atol=1e-8, r=0.05, a=1.0, b=1.0):
    """
      Minimizes the following generalized Huber error metric
           f(x) = 1/a log( exp(a*(y-Cij)) + exp(-(a*(y-Cij)) + b )
      to find elements mu in the covariance matrix. Here y is the scatter (Xt*X).ravel()

    :param s:             state
    :param x:             observation
    :param n_buffer:      length of observation buffer
    :param a:             Huber coefficient
    :param b:             Huber coefficient
    :param n_iter:
    :param atol:          Root finder tolerance
    :return:
    """

    if n_buffer is None:
        n_buffer = s['n_buffer']
    n_dim = len(x)

    try:
        x_prior_centered = x-s['sma']['mean']
    except:
        x_prior_centered = x

    s['sma'] = sma(s=s['sma'],x=x,r=r)
    x_posterior_centered = x-s['sma']['mean']

    x_row = np.atleast_2d(x_posterior_centered)
    x_col = np.transpose(np.atleast_2d(x_posterior_centered))
    y = np.matmul(x_col,x_row).ravel()
    s['buf'] = buf_mean_and_median(s=s['buf'],x=y,n_buffer=n_buffer)

    if len(s['buf']['buffer'])>=2:
        # Minimize Huber loss with just a few iterations, using the previous value
        # It must lie between the median and the mean
        y_mean = s['buf']['mean']
        y_median = s['buf']['median']
        typical_std = np.median(np.std(s['buf']['buffer'], axis=0))
        a_abs = a/typical_std
        s['a']=a_abs

        lb = np.where(y_median < y_mean, y_median, y_mean)
        ub = np.where(y_median > y_mean, y_median, y_mean)
        if s.get('mu') is not None:
            mu0 = s['mu']
            mu0 = np.where( mu0 > lb, mu0, lb )
            mu0 = np.where( mu0 < ub, mu0, ub )
        else:
            mu0 = None
        ys = s['buf']['buffer']
        mu, f_min = parallel_bisection_root_finder(f=huber_deriv, lb=lb, ub=ub, a=a_abs, b=b, xs=ys, n_iter=n_iter, atol=atol, guess=mu0, copy=True)

        s['mu'] = mu/4.0
        # Alternatively...




        DEBUGGING = True
        if DEBUGGING:
            scatter = mean_huber_squared_error(mu=mu, a=a_abs, b=b, xs=ys)
            mu_zero = np.zeros(shape=np.shape(mu))
            zero_scatter = mean_huber_squared_error(mu=mu_zero, a=a_abs, b=b, xs=ys)
            scatter_ratio = scatter/zero_scatter
            from precise.skaters.vectorutil.hubermean import mean_quadratic_error
            sq = mean_quadratic_error(mu=mu,xs=ys)
            sq_zero = mean_quadratic_error(mu=mu_zero,xs=ys)
            sq_ratio = sq/sq_zero
            interesting = {'sq_ratio':sq_ratio,'scatter_ratio':scatter_ratio}
            pprint(interesting)
            pass

        s['pcov'] = np.reshape(mu,newshape=(n_dim,n_dim))

        if DEBUGGING:
            mu_mean = np.nanmean(ys, axis=0)
            s['pcov_e'] = np.reshape(mu_mean,newshape=(n_dim,n_dim))
    return s




