
# Fully autonomous empirical cov skaters

from precise.skaters.exceptions import raise_if_k_not_one
from precise.skaters.covariance.empiricalpre import emp_pcov
from precise.skaters.vector.movingaveragepre import em
import numpy as np


def pcov_emp_d0(y,s:dict,k=1,a=None,t=None,e=None):
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
    if not s or s.get('v'):
        s = {'v':{},                 # <-- vector point estimate
             'c':{}}                 # <-- vector cov estimate
    s['v'] = em(s=s['v'],x=y)        # Update empirical mean
    s['c'] = emp_pcov(s=s['c'],x=y)  # Update empirical cov
    return s['v'], s['pcov'], s


def pcov_emp_d1(y,s:dict,k=1,a=None,t=None,e=None):
    """
            Empirical covariance skater that assumes changes in y's are iid
    """
    if not s or s.get('prev_y'):
        s = {'n_obs':0,
             'prev_y':[],
             'v':{},
             'c':{}}
    s['n_obs']+= 1
    if s['n_obs']>=2:
        dy = y - s['prev_y']
        dy_hat, dy_cov, s = pcov_emp_d0(s=s,y=dy)
        s['prev_y'] = y
        return s['prev_y'] + dy_hat, dy_cov, s
    else:
        return y, np.eye(len(y)), s


EMPIRICAL_COV_SKATERS = [ pcov_emp_d0, pcov_emp_d1 ]


