import numpy as np
import pandas as pd
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef, nearest_pos_def
from precise.skaters.covarianceutil.datascatterfunctions import scatter_tensor_flat
from precise.skaters.covarianceutil.pdutil import data_to_square_dataframe


# Functions that take xs: (n_samples, n_vars) and produce cov matrices, or related
# Can also take a pd.DataFrame whose column names will then be used


def data_population_covariance(xs):
    """
        xs:  (n_samples, n_vars)
        Like np.cov but works if there is only one row
    """
    if isinstance(xs,pd.DataFrame):
        return data_to_square_dataframe(df=xs, data_func=data_population_covariance)
    else:
        if np.shape(xs)[0]==1:
            return np.var(np.array(xs).ravel())*np.eye(1)
        else:
            return np.cov(np.array(xs), rowvar=False, bias=True)


def data_population_correlation(xs):
    """
        Dimension of output is consistent.
    """
    if isinstance(xs, pd.DataFrame):
        return data_to_square_dataframe(df=xs, data_func=data_population_correlation)
    else:
        return cov_to_corrcoef(data_population_covariance(xs))


def scatter_func_cov(xs, cov_loc_func, demean=False, make_pos=True):
    """ Compute covariance using some location function acting on the flattenned scatter data
    :param xs:
    :param cov_loc_func:    Should take 2d array and return a column-wise pseudo-mean (i.e. axis=0)
    :param make_pos:        If True, will ensure cov matrix is pos def
    :param demean:
    :return:
    """
    if isinstance(xs, pd.DataFrame):
        return data_to_square_dataframe(df=xs, data_func=scatter_func_cov, cov_loc_func=cov_loc_func, demean=demean, make_pos=make_pos)
    else:
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

    if isinstance(xs, pd.DataFrame):
        return data_to_square_dataframe(df=xs, data_func=scatter_skater_cov, f=f, demean=demean)
    else:
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
