import numpy as np
from precise.skaters.covarianceutil.conventions import X_TYPE, X_DATA_TYPE, is_data
from precise.skaters.covariance.buffactory import buf_pcov_factory
from precise.skaters.covarianceutil.datafunctions import data_population_covariance
import warnings


def buf_sk_factory(cls, y:X_TYPE=None, s:dict=None,  n_buffer:int=100, n_emp=5, cls_kwargs:dict=None, fit_kwargs:dict=None, e=1):
    """
        :param cls  an sklearn covariance estimating class
        :param n_emp:   If we don't yet have n_emp data points, will revert to empirical
    """

    if cls_kwargs is None:
        cls_kwargs = {}

    if fit_kwargs is None:
        fit_kwargs = {}

    def sk_apply_cov(cls, xs, cls_kwargs:dict, fit_kwargs:dict, n_emp:int):

        if len(xs) < n_emp:
            try:
                _pcov = data_population_covariance(xs)
            except:
                _pcov = np.eye(len(xs))
            try:
                _location = np.nanmean(xs,axis=0)
            except:
                _location = np.zeros(len(xs))
            outputs = {'loc':_location,'pcov':_pcov}
        else:
            obj = cls(**cls_kwargs)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                obj.fit(np.array(xs),**fit_kwargs)
            try:
                outputs = {'loc': obj.location_, 'pcov': obj.covariance_}
            except AttributeError:
                print('obj lacks ._location or ._covariance')
                raise
        return outputs

    func = lambda xs: sk_apply_cov(cls=cls, xs=xs, fit_kwargs=fit_kwargs, n_emp=n_emp, cls_kwargs=cls_kwargs)
    return buf_pcov_factory( func=func, y=y, s=s, n_buffer=n_buffer, e=e)