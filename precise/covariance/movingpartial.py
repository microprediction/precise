import numpy as np
from precise.covariance.movingaverage import _ema_scov_update, _ema_scov_init
from typing import Union, List
from precise.vector.switchingaverage import sma

# Running average scatter estimate based on partial moments
# If no target is supplied, either initially or for the update call, then a running mean will be used.

# Don't use. BUGGY.

QUADRANTS = {'cu':(1.0,1,1),    # x*1 > 0  y*1 > 0
             'du':(-1.0,-1,1),
             'dl':(-1.0,1,-1),
             'cl':(1.0,-1,-1)}


def pema_scov(s:dict, x:Union[List[float], int]=None, r:float=0.025):
    """ Maintain running population covariance """
    target = 0
    if s.get('n_samples') is None:
        if isinstance(x,(int,float)):
            return _pema_scov_init(n_dim=int(x),r=r,target=target)
        elif len(x)>1:
            s = _pema_scov_init(n_dim=len(x),r=r,target=target)
        else:
            raise ValueError('Not sure how to initialize EWA COV tracker. Supply x=5 say, for 5 dim')
    if x is not None:
        s = _ema_scov_update(s=s, x=x, r=r)
    return s


def _pema_scov_init(n_dim=None, r:float=0.025, n_emp=None, target:float=None )->dict:
    """ Initialize object to track partial moments

       r:       Importance of current data point
       n_emp:   Discouraged. Really only used for tests.
                This is the number of samples for which empirical is used, rather
                than running updates. By default n_emp ~ 1/r

    """
    s = dict([ (q,_ema_scov_init(n_dim=n_dim,r=r,n_emp=n_emp)) for q in QUADRANTS ])
    q = next(iter(s.keys())) # Choose any
    s['n_dim'] = s[q]['n_dim']
    s['target'] = target
    s['sma'] = sma({},n_dim,r=r)
    return s


def _pema_scov_update(s:dict, x:[float], r:float=None, target=None):
    """ Update recency weighted estimate of scov-like matrix by treating quadrants individually """

    assert len(x)==s['n_dim']
    s['sma'] = sma(s=s['sma'], x=x, r=r)

    # If target is not supplied we maintain a mean that switches from emp to ema
    if target is None:
        target = s['target']
    if target is None:
        target = s['sma']['mean']

    # Update running partial scatter estimates
    for q,(w,sgn1,sgn2) in QUADRANTS.items():
        x1 = (x-target)*sgn1
        x2 = (x-target)*sgn2
        x1[x1<0]=0
        x2[x2<0]=0
        x1 = sgn1*x1
        x2 = sgn2*x2
        s[q] = _ema_scov_update(s[q],x=x1,r=r,target=0, y=x2)

    s['scov'] = np.zeros(shape=((s['n_dim'],s['n_dim'])))
    for q in QUADRANTS:
        s['scov'] += s[q]['scov']
    s['mean'] = np.copy( s['sma']['mean'] )
    return s






