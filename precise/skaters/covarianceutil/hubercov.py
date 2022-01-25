from precise.skaters.locationutil.hubermean import huber_mean
from precise.skaters.covarianceutil.datacovfunctions import scatter_func_cov
import numpy as np
from pprint import pprint


def scatter_huber_cov(xs, a ,b ,n_iter=20, atol=1e-8, demean=False):
    """ Huber cov """
    def hloc(xs):
        return huber_mean(xs=xs, a=a, b=b, n_iter=n_iter, atol=atol)

    return scatter_func_cov(xs=xs, cov_loc_func=hloc, demean=demean)


def scatter_emp_cov(xs, demean=False):
    """ Empirical cov """
    # Here mostly as a check
    def mloc(xs):
        return xs[0] if len(xs )==1 else np.nanmean(xs ,axis=0)
    return scatter_func_cov(xs=xs, cov_loc_func=mloc)


if __name__=='__main__':
    xs = np.random.randn(20,4)
    ce = scatter_emp_cov(xs=xs, demean=True)
    ch = scatter_huber_cov(xs=xs, demean=True)
    pprint(ce)
    pprint(ch)
