import numpy as np
from precise.covariance.recent import rcov_update, rcov_init

# Track running expon weighted cov estimates using a known sub-division

def lz_rcov_init(adj, n_emp=10, rho=0.05):
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
    m['states'] = [rcov_init(n_dim=nd, n_emp=n_emp, rho=rho) for nd in n_dims]
    return m

def lz_rcov_update(m:dict, x:[float])->dict:
    """ Update one cov dict for each variable """
    for i,r in enumerate(m['states']):
        indx = m['adj'][:, i]
        xi = x[indx]
        r = rcov_update(m=r,x=xi)
    return m









