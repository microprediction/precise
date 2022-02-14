import numpy as np
from precise.skaters.covariance.runempfactory import _emp_pcov_init, _emp_pcov_update
import math
from typing import Union, List

# Exponential weighted sample covariance


def ewa_emp_pcov_factory(y, s:dict, k=1, r=0.025, n_emp=None, e=1):
    assert k==1
    s = ema_scov(s=s,x=y,r=r, n_emp=n_emp)
    x = s['mean']
    x_cov = s['pcov']
    return x, x_cov, s


def ema_scov(s:dict, x:Union[List[float], int]=None, r:float=0.025, n_emp=None):
    """ Maintain running population covariance """
    if s.get('n_samples') is None:
        if isinstance(x,int):
            return _ema_scov_init(n_dim=x,r=r, n_emp=n_emp)
        elif isinstance(x,(List,np.ndarray)):
            s = _ema_scov_init(n_dim=len(x),r=r, n_emp=n_emp)
        else:
            raise ValueError('Not sure how to initialize EWA COV tracker. Supply x=5 say, for 5 dim')
    if x is not None:
        s = _ema_scov_update(s=s, x=x, r=r)
    return s


def _ema_scov_init(n_dim=None, r:float=0.025, n_emp=None ):
    """ Initialize object to track exp moving avg cov for zero mean

       r:       Importance of current data point
       n_emp:   Discouraged. Really only used for tests.
                This is the number of samples for which empirical is used, rather
                than running updates. By default n_emp ~ 1/r

    """
    if n_emp is None:
        n_emp = int(min(250, max(5, math.ceil(1 / r))))
    s = _emp_pcov_init(n_dim=n_dim)
    s.update({'rho':r, 'n_emp':n_emp})
    return s


def _ema_scov_update(s:dict, x:[float], r:float=None, target=None, y=None):
    """ Update recency weighted estimate of scov for zero mean

          If target is not None, it will be used in place of the mean when updating
          Obviously, this changes the interpretation of 'scov'

          xt - transpose of x

    """
    if s['n_samples']< s['n_emp']:
        # Use the regular cov update for a burn-in period
        # During this time both scov and pcov are maintained
        s = _emp_pcov_update(s=s, x=x, target=target)
        if s['n_samples']>1:
            s['scov'] = s['pcov'] * s['n_samples'] / (s['n_samples'] - 1)
    else:
        s['n_samples']+=1
        r = s['rho'] if r is None else r
        assert s['n_dim'] == len(x)
        xcol = np.ndarray(shape=(s['n_dim'], 1))
        if target is not None:
             xcol[:,0] = x - target
        else:
            xcol[:,0] = x - s['mean']
        if y is None:
            ycolT = xcol.T
        else:
            ycol = np.ndarray(shape=(s['n_dim'], 1))
            if target is not None:
                ycol[:, 0] = y - target
            else:
                ycol[:, 0] = y - s['mean']
            ycolT = ycol.T

        yyt = np.dot(xcol, ycolT)
        s['scov'] = (1 - r) * s['scov'] + r * yyt
        s['mean'] = (1 - r) * s['mean'] + r * x
        s['pcov']= s['scov']*(s['n_samples']-1)/s['n_samples']
    return s





