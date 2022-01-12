import numpy as np
from precise.covariance.movingaverage import _ema_scov_update, _ema_scov_init

# Track running expon weighted cov estimates using a known sub-division


# 1. Variable by variable cov tracking

def _lz_scov_init(adj, n_emp=10, rho=0.05):
    """ Minimal steps to ensure adjacency matrix is okay,
         and initialize one cov tracker for each variable.

    :param adj:     Adjacency matrix. Only positivity will be used.
    :param n_emp:   Number of data points to use empirical cov before switching to expon weighted
    :return:
    """
    n_dim, n_dim_check = np.shape(adj)
    assert n_dim==n_dim_check
    adj = np.vectorize(float)(adj > 0)
    m = dict()
    m['adj'] = adj.astype(bool)
    n_dims = [int(s) for s in np.sum(adj,axis=0)]
    m['states'] = [_ema_scov_init(n_dim=nd, n_emp=n_emp, r=rho) for nd in n_dims]
    return m


def _lz_scov_update(m:dict, x:[float])->dict:
    """ Update one cov dict for each variable """
    for i,r in enumerate(m['states']):
        indx = m['adj'][:, i]
        xi = x[indx]
        r = _ema_scov_update(s=r, x=xi)
    return m











