import numpy as np
from precise.skaters.covarianceutil.conventions import X_TYPE
from precise.skaters.covariance.bufferedpre import buf_mean_and_pcov
from precise.skaters.covarianceutil.differencing import d1_factory

# Simple, inefficient skaters that use operations on a buffer of past values


def buf_pcov_d0(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """
        Empirical covariance skater that assumes y's are iid

    :param y:  (n_dim,)   Incoming vector of observations
    :param s:             State
    :param k:             Steps ahead to predict (this won't change anything)
    :param a:             Variables know in advance (ignored)
    :param t:             Epoch time (ignored)
    :param e:             Allocated computation time (ignored)
    :return:  (n_dim,), (n_dim,n_dim), dict
              Point estimate, cov estimate, posterior state
    """
    s = buf_mean_and_pcov(s=s, x=y, n_buffer=n_buffer)
    x = s['mean']
    x_cov = s['pcov']
    return x, x_cov, s


def buf_pcov_d1( y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """
        For when changes are iid gaussian
    """
    return d1_factory( f = buf_pcov_d0, y=y, s=s, n_buffer=n_buffer )


def buf_pcov_d1_long_form(s:dict=None, y:X_TYPE=None, n_buffer:int=100):
    # A long form version of the above, just for clarity and testing
    if not s or s.get('dy'):
        s = {'prev_y': y,
             'dy': {}}
        return y, np.eye(len(y)), s
    else:
        dy = y - s['prev_y']
        dy_hat, dy_cov, s['dy'] = buf_pcov_d0(y=dy, s=s['dy'], n_buffer=n_buffer)
        y['prev_y'] = y
        x = s['prev_y'] + dy_hat
        return x, dy_cov, s