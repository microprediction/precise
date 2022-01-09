# Precision estimation with known block structure Le & Zhong
import numpy as np
from precise.covariance.recent import rcov_update, rcov_init

def known_rcov_init(adjacency, n_cold=10, rho=0.05):
    """ Initialize state object to track known exp weighted precision
        This version assumes membership is constant
    :param adjacency:  Adjacency matrix
    :return:
    """
    n_dim, n_dim_check = np.shape(adjacency)
    assert n_dim==n_dim_check
    adj = np.vectorize(float)(adjacency>0)
    m = dict()
    m['adj'] = adj.astype(bool)
    m['n_dims'] = [int(s) for s in np.sum(adj,axis=0)]
    m['states'] = [ rcov_init(n_dim=nd, n_cold=n_cold, rho=rho) for nd in m['n_dims'] ]
    return m

def known_rcov_update(m, x):
    for i,r in enumerate(m['states']):
        indx = m['adj'][:, i]
        xi = x[indx]
        r = rcov_update(m=r,x=xi)
    return m










