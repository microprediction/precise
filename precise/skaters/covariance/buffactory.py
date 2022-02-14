import numpy as np
from precise.skaters.covarianceutil.conventions import X_TYPE, X_DATA_TYPE, is_data
from precise.skaters.covarianceutil.datafunctions import data_population_covariance, data_population_correlation

# State machines that track stats for finite buffers of vectors


def buf_pcov_factory(func, y:X_TYPE=None, s:dict=None, n_buffer:int=100, e=1):
    """
         Factory for building estimators from functions that return dicts with 'loc' and 'pcov' keys

    :param func:  Acts on buffer and returns object with 'loc', 'pcov'
    :param y:
    :param s:
    :param n_buffer:
    :return:
    """
    s = _buf(funcs=[func], func_names=['mav'], func_kwargs=[{}],s=s, x=y, n_buffer=n_buffer, e=e)
    if s.get('mav') is not None:
        x = np.array(s['mav']['loc'])
        x_cov = np.array(s['mav']['pcov'])
    else:
        x = y
        x_cov = np.eye(len(y))
    return x, x_cov, s


def buf_cov(s:dict=None, x:X_TYPE=None, n_buffer:int=100)->dict:
    # Equivalent to np.nanstd(xs[max(0, k - n_buffer + 1):k + 1], axis=0)
    return _buf1(func=data_population_correlation, func_name='corrcoef', s=s, x=x, n_buffer=n_buffer)


def buf_std(s:dict=None, x:X_TYPE=None, n_buffer:int=100)->dict:
    # Equivalent to np.nanstd(xs[max(0, k - n_buffer + 1):k + 1], axis=0)
    return _buf1(func=np.nanstd, func_name='mean', s=s, x=x, n_buffer=n_buffer, axis=0)


def buf_mean(s:dict=None, x:X_TYPE=None, n_buffer:int=100)->dict:
    # Equivalent to np.nanmean(xs[max(0, k - n_buffer + 1):k + 1], axis=0)
    return _buf1(func=np.nanmean, func_name='mean', s=s, x=x, n_buffer=n_buffer, axis=0)


def buf_median(s:dict=None, x:X_TYPE=None, n_buffer:int=100)->dict:
    # Equivalent to np.nanmedian(xs[max(0, k - n_buffer + 1):k + 1], axis=0)
    return _buf1(func=np.nanmedian, func_name='median', s=s, x=x, n_buffer=n_buffer, axis=0)


def _buf1(func, func_name, s:dict=None, x:X_TYPE=None, n_buffer:int=100, e=1, **func_kwarg)->dict:
    return _buf(funcs=[func], func_names=[func_name], func_kwargs=[func_kwarg], s=s, x=x, n_buffer=n_buffer,e=e)


def buf_mean_and_median(s:dict=None, x:X_TYPE=None, n_buffer:int=100, e=1)->dict:
    return _buf(funcs=[np.nanmean, np.nanmedian], func_names=['mean','median'], func_kwargs=[{'axis':0},{'axis':0}], s=s, x=x, n_buffer=n_buffer, e=e)


def buf_mean_and_pcov(s:dict=None, x:X_TYPE=None, n_buffer:int=100, e=1)->dict:
    # Equivalent to np.cov(xs[max(0, k - n_buffer + 1):k + 1], axis=0)
    return _buf(funcs=[np.nanmean, data_population_covariance], func_names=['mean', 'pcov'], func_kwargs=[{'axis':0}, {}], s=s, x=x, e=e, n_buffer=n_buffer)


def _buf(funcs, func_names:[str], func_kwargs:[dict], s:dict=None, x:X_TYPE=None, n_buffer:int=100, e=1)->dict:
    """
    :param funcs:            [func(xs, axis=0) -> 1d array]
    :param func_names:
    :param s:
    :param x:
    :param n_buffer:
    :param e:             If e>1 calculation is performed
    :return:
    """
    if not s:
        s = _buf_init(s=s, n_buffer=n_buffer)
    if is_data(x):
        s = _buf_update(funcs=funcs, func_names=func_names, func_kwargs=func_kwargs, s=s, x=x, n_buffer=n_buffer, e=e)
    return s


def _buf_init(s:dict=None, n_buffer:int=None)->dict:
    if not s:
        s = dict()
    s.update( {'buffer':list(), 'n_buffer':n_buffer} )
    return s


def _buf_update(funcs, func_names, func_kwargs, s:dict, x:X_DATA_TYPE, n_buffer:int=None, e=1)->dict:
    if n_buffer is None:
        n_buffer = s['n_buffer']
    if len(s['buffer']):
        assert len(s['buffer'][0])==len(x), 'dimension mismatch'
    s['buffer'].append(np.atleast_1d(x))
    if len(s['buffer'])>n_buffer:
        _ = s['buffer'].pop(0)
    for func, func_name, func_kwargs in zip(funcs, func_names, func_kwargs):
        if e>0:
            s[func_name] = func(s['buffer'],**func_kwargs)
    return s




if __name__=='__main__':
    import random
    xs = np.random.randn(500,100)
    xs[17,1] = np.nan
    s = {}
    n_buffer = random.choice([1,5,100])
    for k,x in enumerate(xs):
        s = buf_mean_and_median(s=s, x=x, n_buffer=n_buffer)
        np_median = np.nanmedian(xs[max(0,k-n_buffer+1):k+1], axis=0)
        s_median = s['median']
        if not np.allclose( np_median, s_median, atol=1e-8 ):
            print('urgh')
            assert False
