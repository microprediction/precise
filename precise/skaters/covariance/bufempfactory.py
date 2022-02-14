from precise.skaters.covariance.buffactory import buf_mean_and_pcov
from precise.skaters.covarianceutil.conventions import Y_DATA_TYPE
import numpy as np

def buf_emp_pcov_d0_factory(y:Y_DATA_TYPE, s:dict, n_buffer:int=100, e=1):
    """
        Empirical covariance skater that assumes y's are iid

    :param y:  (n_dim,)   Incoming vector of observations
    :param s             State
    :param k:             Steps ahead to predict (this won't change anything)
    :param a:             Variables know in advance (ignored)
    :param t:             Epoch time (ignored)
    :param e:             Allocated computation time (ignored)
    :return:  (n_dim,), (n_dim,n_dim), dict
              Point estimate, cov estimate, posterior state
    """
    s = buf_mean_and_pcov(s=s, x=y, n_buffer=n_buffer, e=e)
    try:
        x = s['mean']
    except KeyError:
        x = y

    try:
        x_cov = s['pcov']
    except KeyError:
        x_cov = np.eye(len(y))

    return x, x_cov, s
