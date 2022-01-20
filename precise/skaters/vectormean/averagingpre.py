import numpy as np
from precise.skaters.covarianceutil.conventions import X_TYPE, X_DATA_TYPE, is_data, infer_dimension

# Running means for vectors


def ewa(s:dict=None, x:X_TYPE=None, r:float=0.025, n_dim:int=None):
    """ Exponential weighted average """
    return averager(s=s, x=x, r=r, n_dim=n_dim, method='ma')


def sma(s:dict=None, x:X_TYPE=None, r:float=0.025, n_dim:int=None):
    """ Switching from empirical to ewa """
    return averager(s=s, x=x, r=r, n_dim=n_dim, method='switch')



def averager(s:dict=None, x:X_TYPE=None, r:float=0.025, method:str= 'switch', n_dim:int=None):
    """ Stands for "switching moving average"
          method:   'switch', 'ma' or 'emp'
    """
    if not s:
        s = _sma_init(s=s,x=x,r=r,n_dim=n_dim, method=method)
    if is_data(x):
        s = _sma_update(s=s,x=x,r=r, method=method)
    return s


def _sma_init(s:dict=None, x:X_TYPE=None, n_dim:int=None, r=None, method:str=None):
    n_dim = infer_dimension(n_dim=n_dim, x=x)
    if not s:
        s = dict()
    s.update( {'n_samples':0,'mean':np.zeros(n_dim),'r':r,'method':method})
    return s


def _sma_update(s:dict, x:X_DATA_TYPE, r=None, method:str=None):
    method = method or s['method']
    r = r if (r is not None) else s['r']
    s['n_samples'] += 1
    if (s['n_samples']<1/r and method=='switch') or (method=='emp'):
        s['mean'] += x/s['n_samples']
    else:
        if s['n_samples']==1:
            s['mean'] = x
        else:
            s['mean'] = (1-r)*s['mean'] + r*x
    return s



