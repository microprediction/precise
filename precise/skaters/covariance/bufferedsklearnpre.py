import numpy as np
from precise.skaters.covarianceutil.conventions import X_TYPE, X_DATA_TYPE, is_data
from precise.skaters.covariance.bufferedpre import buf_pcov_factory


def buf_sk_factory(cls, y:X_TYPE=None, s:dict=None,  n_buffer:int=100, **kwargs):
    """
        :param cls  an sklearn covariance estimating class
    """

    def sk_apply_cov(cls, xs):
        obj = cls().fit(xs)
        return {'loc': obj._location, 'pcov': obj._covariance}

    func = lambda xs: sk_apply_cov(cls=cls, xs=xs, **kwargs)
    return buf_pcov_factory( func=func, y=y, s=s, n_buffer=n_buffer)