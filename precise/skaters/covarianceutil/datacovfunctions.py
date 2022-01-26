import numpy as np
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef, nearest_pos_def
from precise.skaters.covarianceutil.datascatterfunctions import scatter_tensor_flat


# Functions that take xs: (n_samples, n_vars) and produce cov matrices, or related


def pcov_of_columns(xs):
    """
        Dimension of out put is consistent. c.f. np.cov( )
    """
    if any([dim == 1 for dim in np.shape(xs)]):
        n_dim = max(np.shape(xs))
        return np.eye(n_dim)
    else:
        return np.cov(np.array(xs), rowvar=False, bias=True)


def np_pcorrcoef(xs):
    """
        Dimension of output is consistent.
    """
    return cov_to_corrcoef(pcov_of_columns(xs))


def scatter_func_cov(xs, cov_loc_func, demean=False, make_pos=True):
    """ Compute covariance using some location function acting on the flattenned scatter data
    :param xs:
    :param cov_loc_func:    Should take 2d array and return a column-wise pseudo-mean (i.e. axis=0)
    :param make_pos:        If True, will ensure cov matrix is pos def
    :param demean:
    :return:
    """
    n_samples, n_dim = np.shape(xs)
    if n_samples<=2:
        return np.eye(n_dim)
    else:
        stf = scatter_tensor_flat(xs=xs, demean=demean)  # (n_samples, n_dim*n_dim )
        assert np.shape(stf)[1]==n_dim*n_dim
        loc = cov_loc_func(stf)
        cov = np.reshape(loc, newshape=(n_dim, n_dim))
        if make_pos:
            cov = nearest_pos_def(a=cov)
        return cov


def scatter_skater_cov(xs, f, demean=False):
    """ Compute covariance using a univariate skater function on the flattened scatter data entries """

    def skater_func(xs_):
        n_samples, n_entries = np.shape(xs_)
        final_x = list()
        for j in range(n_entries):
            s = {}
            x = np.squeeze(xs_[:, j])
            for y in x:
                x, x_std, s = f(s=s, y=y, k=1)
            final_x.append(x)
        return np.array(final_x)

    return scatter_func_cov(xs=xs, cov_loc_func=skater_func, demean=demean)
