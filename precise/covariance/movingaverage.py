import numpy as np
from precise.covariance.empirical import _emp_pcov_init, _emp_pcov_update
import math
from typing import Union, List

# Exponential weighted sample covariance


def _ema_scov_init(n_dim=None, r:float=0.025, n_emp=None ):
    """ Initialize object to track exp moving avg cov

       r:       Importance of current data point
       n_emp:   Discouraged. Really only used for tests.
                This is the number of samples for which empirical is used, rather
                than running updates. By default n_emp ~ 1/r

    """
    if n_emp is None:
        n_emp = int(min(50, max(5, math.ceil(1 / r))))
    s = _emp_pcov_init(n_dim=n_dim)
    s.update({'rho':r, 'n_emp':n_emp})
    return s


def _ema_scov_update(s:dict, x:[float], r:float=None):
    """ Update recency weighted estimate of scov """
    if s['n_samples']< s['n_emp']:
        # Use the regular cov update for a burn-in period
        # During this time both scov and pcov are maintained
        s = _emp_pcov_update(s=s, x=x)
        s['scov'] = s['pcov'] * (s['n_samples'] - 1) / s['n_samples']
    else:
        s['n_samples']+=1
        r = s['rho'] if r is None else r
        assert s['n_dim'] == len(x)
        ycol = np.ndarray(shape=(s['n_dim'], 1))
        ycol[:,0] = x - s['mean']
        yyt = np.dot(ycol, ycol.T)
        s['scov'] = (1 - r) * s['scov'] + r * yyt
        s['mean'] = (1 - r) * s['mean'] + r * x
        s['pcov']=None # Invaliate stale pcov if it exists
    return s


def ema_scov(s:dict, x:Union[List[float], int]=None, r:float=0.025):
    """ Maintain running population covariance """
    if s.get('n_samples') is None:
        if isinstance(x,int):
            return _ema_scov_init(n_dim=x,r=r)
        elif len(x)>1:
            s = _ema_scov_init(n_dim=len(x),r=r)
        else:
            raise ValueError('Not sure how to initialize EWA COV tracker. Supply x=5 say, for 5 dim')
    if x is not None:
        s = _ema_scov_update(s=s, x=x, r=r)
    return s




