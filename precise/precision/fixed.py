
# Provides running estimate of precision matrix using known sub-division
# Simple algo whose theoretical properties are discussed by Le and Zhong in
# the paper "High-Dimensional Precision Matrix Estimation with a Known Graphical Structure"

from precise.covariance.fixed import fixed_rcov_init, fixed_rcov_update
import numpy as np
from precise.covariance.util import multiply_diag, grand_shrink


def fixed_rpre_init(adj, n_emp=10, rho=0.05):
    m = fixed_rcov_init(adj=adj, n_emp=n_emp, rho=rho)
    n_dim = np.shape(adj)[0]
    for i,r in enumerate(m['states']):
        nd = r['n_dim']
        B = np.zeros(shape=(n_dim,nd))
        ndxs = m['adj'][:,i]
        B[ndxs,:] = np.eye(nd)
        r['B'] = B
    return m


def fixed_rpre_update(m, x, with_precision=True, lmbd=0.3, phi=1.3):
    m = fixed_rcov_update(m,x)
    n_dim = np.shape(m['adj'])[0]
    omega = np.zeros(shape=(n_dim,n_dim))
    if with_precision:
        cnt = m['states'][0]['count']
        if cnt<2:
            omega = np.eye(n_dim)
        else:
            for i,r in enumerate(m['states']):
                R = multiply_diag(r['cov'], phi=phi, make_copy=True)
                R = grand_shrink(R, lmbd=lmbd, make_copy=True)
                Sinv = np.linalg.inv(R)
                ei = np.zeros(shape=(n_dim,1))
                ei[i] = 1.0
                B = r['B']
                fi = np.matmul(B.T,ei)
                Sfi = np.matmul(Sinv,fi)
                wi = np.matmul(B,Sfi)
                omega[:,i] = wi[:,0]
    m['pre'] = omega
    return m






