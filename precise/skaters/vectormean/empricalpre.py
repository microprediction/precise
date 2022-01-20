from precise.skaters.covarianceutil.conventions import X_TYPE
from precise.skaters.vectormean.averagingpre import averager


def emp(s:dict=None, x:X_TYPE=None):
    """ Empirical mean """
    return averager(s=s, x=x, method='emp')