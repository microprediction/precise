import numpy as np


def sma(s:dict=None, x=None, r:float=0.025):
    """ Mean estimator switching from empirical to moving average """
    if (s is None) or s.get('n_samples') is None:
        if isinstance(x,int):
            n_dim = x
        else:
            n_dim = len(x)
        s = {'n_samples':0,'mean':np.zeros(n_dim),'r':r}
    if (x is not None) and not isinstance(x,int):
        if r is None:
            r = s['r']
        if r is None:
            raise Exception('r must be supplied at initialization, or on the fly')
        s['n_samples'] += 1
        if s['n_samples']<1/r:
            s['mean'] += x/s['n_samples']
        else:
            s['mean'] = (1-r)*s['mean'] + r*x
    return s
