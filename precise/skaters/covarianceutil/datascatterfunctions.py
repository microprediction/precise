
# Utilities for when data is presented as (n_samples, n_vars)

import numpy as np


def scatter_tensor(xs, demean=False):
    """ Returns all the individual scatter matrices

    :param xs:           (n_samples, n_vars)
    :param demean:
    :return: (n_samples, n_vars, n_vars )
    """
    if demean:
        b = xs - np.mean(np.array(xs), axis=0)
    else:
        b = xs
    b_rows = np.atleast_3d(b)
    b_cols = np.transpose(b_rows, axes=[0, 2, 1])
    sc = np.matmul(b_rows, b_cols)
    return sc


def scatter_tensor_flat(xs, demean=False):
    """ Flat scatter
    :param xs:  (n_samples, n_vars)
    :param demean:
    :return:    (n_samples, n_vars*n_vars )
    """
    sc = scatter_tensor(xs=xs, demean=demean)
    [n_samples, n_dim, n_dim_check] = np.shape(sc)
    assert n_dim == n_dim_check
    return np.reshape(sc, newshape=[n_samples, n_dim * n_dim])



if __name__=='__main__':
    a = np.random.randn(10,3)
    scatter_tensor(a, demean=True)