
# Provides running estimate of precision matrix using known sub-division
# Simple algo whose theoretical properties are discussed by Le and Zhong in
# the paper "High-Dimensional Precision Matrix Estimation with a Known Graphical Structure"

from precise.covariance.lezhong import _lz_scov_init, _lz_scov_update
import numpy as np
from precise.covariance.matrixfunctions import multiply_diag, grand_shrink


# Uses moving average estimate of sub-covariance matrices


def _lz_ema_spre_init(adj:np.ndarray, n_emp=10, rho=0.05)->dict:
    """ Le-Zhong state initialization
    :param adj:     n_dim x n_dim adjacency matrix
    :param n_emp:   number of observations before switching from emp to moving avg cov
    :param rho:     importance of most recent observation
    :return:
    """
    m = _lz_scov_init(adj=adj, n_emp=n_emp, rho=rho)
    n_dim = np.shape(adj)[0]
    for i,r in enumerate(m['states']):
        nd = r['n_dim']
        B = np.zeros(shape=(n_dim,nd))
        ndxs = m['adj'][:,i]
        B[ndxs,:] = np.eye(nd)
        r['B'] = B
    return m


def _lz_ema_spre_update(m:dict, x:[float], update_precision=True, lmbd=0.3, phi=1.3)->dict:
    """ Update Le-Zhong state by updating collection of cov estimates
    :param m:                 Prior state
    :param x:                 Observations
    :param update_precision:  If True, a precision matrix will be upated.
    :param lmbd:              Shrinkage parameter (applied to uI)
    :param phi:               Diagonal multiplier
    :returns m  {'spre':...}
    """
    m = _lz_scov_update(m, x)
    n_dim = np.shape(m['adj'])[0]
    omega = np.zeros(shape=(n_dim,n_dim))
    if update_precision:
        cnt = m['states'][0]['n_samples']
        if cnt<2:
            omega = np.eye(n_dim)
        else:
            for i,r in enumerate(m['states']):
                R = multiply_diag(r['scov'], phi=phi, copy=True)
                R = grand_shrink(R, lmbd=lmbd, copy=True)
                Sinv = np.linalg.inv(R)
                ei = np.zeros(shape=(n_dim,1))
                ei[i] = 1.0
                B = r['B']
                fi = np.matmul(B.T,ei)
                Sfi = np.matmul(Sinv,fi)
                wi = np.matmul(B,Sfi)
                omega[:,i] = wi[:,0]
    m['spre'] = omega
    return m


# Second version is more general

def glz_init(adj, cov_init, **kwargs):
    """ Stands for "General Le-Zhong"

          _emp_pcov_init(n_dims,**kwargs) creates cov tracking state
          kwargs : arguments passed to cover_init, in addition to n_dim

    """
    n_dim, n_dim_check = np.shape(adj)
    assert n_dim == n_dim_check
    adj = np.vectorize(float)(adj > 0)
    m = dict()
    m['adj'] = adj.astype(bool)
    n_dims = [int(s) for s in np.sum(adj, axis=0)]
    m['states'] = [cov_init(n_dim=nd, **kwargs) for nd in n_dims]

    n_dim = np.shape(adj)[0]
    for i,r in enumerate(m['states']):
        nd = r['n_dim']
        B = np.zeros(shape=(n_dim,nd))
        ndxs = m['adj'][:,i]
        B[ndxs,:] = np.eye(nd)
        r['B'] = B
    return m


def glz_update(m:dict, x, cov_update, cov_transform=None, with_precision=True):
    """
    :param m:  state
    :param x:  observed data
    :param cov_update(m,x)
    :param with_precision:
    :param update_kwargs:
    :return:
    """

    # Update the covariance states
    for i,r in enumerate(m['states']):
        indx = m['adj'][:, i]
        xi = x[indx]
        r = cov_update(m=r,x=xi)

    # Create precision matrices column-wise and combine
    n_dim = np.shape(m['adj'])[0]
    omega = np.zeros(shape=(n_dim,n_dim))
    if with_precision:
        cnt = m['states'][0]['n_samples']
        if cnt<2:
            omega = np.eye(n_dim)
        else:
            for i,r in enumerate(m['states']):
                if cov_transform is not None:
                    R = cov_transform(np.copy(r['cov']))
                    Sinv = np.linalg.inv(R)
                    ei = np.zeros(shape=(n_dim,1))
                    ei[i] = 1.0
                    B = r['B']
                    fi = np.matmul(B.T,ei)
                    Sfi = np.matmul(Sinv,fi)
                    wi = np.matmul(B,Sfi)
                    omega[:,i] = wi[:,0]
    m['spre'] = omega
    return m



