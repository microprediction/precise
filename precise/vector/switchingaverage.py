import numpy as np


def sma(s:dict=None, x=None, r:float=0.025):
    """ Mean estimator switching from empirical to moving average """
    if (s is None) or s.get('count') is None:
        if isinstance(x,int):
            n_dim = x
        else:
            n_dim = len(x)
        s = {'count':0,'mean':np.zeros(n_dim),'r':r}
    if x is not None:
        if r is None:
            r = s['r']
        if r is None:
            pass
            raise Exception('r must be supplied at initialization, or on the fly')
        s['count'] += 1
        rho = max(r, 1/s['count'])
        s['mean'] = (1-rho)*s['mean'] + rho*x
    return s
