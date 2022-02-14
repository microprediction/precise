import numpy as np
from precise.skaters.covarianceutil.hubercov import scatter_huber_cov
from precise.skaters.covariance.buffactory import _buf
from precise.skaters.covarianceutil.conventions import X_TYPE


def buf_huber_d0_factory(s,y,n_buffer, a,b,n_iter=20, atol=1e-8, e=1):
    s = buf_mean_and_huber_pcov(s=s,x=y, a=a,b=b, n_iter=n_iter, atol=atol, n_buffer=n_buffer, e=e)
    try:
        x = s['mean']
        x_cov = s['pcov']
    except KeyError:
        x = np.array(y)
        x_cov = np.eye(len(y))

    return x, x_cov, s


def buf_mean_and_huber_pcov(s:dict=None, x:X_TYPE=None, n_buffer:int=100,a=1.0, b=2.0,n_iter=20, atol=1e-8, e=1)->dict:
    # Similar to np.cov(xs[max(0, k - n_buffer + 1):k + 1], axis=0) but uses Huber location for cov estimate

    def hcov(xs_):
        return scatter_huber_cov(xs=xs_, a=a,b=b, n_iter=n_iter, atol=atol, demean=True)

    return _buf(funcs=[np.nanmean, hcov], func_names=['mean', 'pcov'], func_kwargs=[{'axis':0}, {}], s=s, x=x, n_buffer=n_buffer, e=e)
