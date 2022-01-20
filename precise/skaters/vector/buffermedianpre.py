import numpy as np
from precise.skaters.covarianceutil.conventions import X_TYPE, X_DATA_TYPE, is_data


# Vectorized median for finite buffer
# Equivalent to np.nanmedian(xs[max(0,k-n_buffer+1):k+1], axis=0)


def med(s:dict=None, x:X_TYPE=None, n_buffer:int=100 ):
    if not s:
        s = _med_init(s=s, n_buffer=n_buffer)
    if is_data(x):
        s = _med_update(s=s, x=x)
    return s


def _med_init(s:dict=None, n_buffer:int=None):
    if not s:
        s = dict()
    s.update( {'buffer':list(), 'n_buffer':n_buffer} )
    return s


def _med_update(s:dict, x:X_DATA_TYPE, n_buffer:int=None):
    if n_buffer is None:
        n_buffer = s['n_buffer']
    if len(s['buffer']):
        assert len(s['buffer'][0])==len(x), 'dimension mismatch'
    s['buffer'].append(np.atleast_1d(x))
    if len(s['buffer'])>n_buffer:
        _ = s['buffer'].pop(0)
    s['median'] = np.nanmedian(s['buffer'],axis=0)
    return s



if __name__=='__main__':
    import random
    xs = np.random.randn(500,100)
    xs[17,1] = np.nan
    s = {}
    n_buffer = random.choice([1,5,100])
    for k,x in enumerate(xs):
        s = med(s=s,x=x,n_buffer=n_buffer)
        np_median = np.nanmedian(xs[max(0,k-n_buffer+1):k+1], axis=0)
        s_median = s['median']
        if not np.allclose( np_median, s_median, atol=1e-8 ):
            print('urgh')
            assert False
