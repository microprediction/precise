import numpy as np
import math
import pandas as pd
from precise.skaters.covarianceutil.pdutil import square_to_square_dataframe, square_to_column_series, square_to_index_series

# Functions acting on cov, corrcoef matrices and other square matrices
# If square pd.DataFrame are supplied instead, index and columns are preserved


def cov_to_corrcoef(a):
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, cov_to_corrcoef)
    else:
        variances = np.diagonal(a)
        denominator = np.sqrt(variances[np.newaxis, :] * variances[:, np.newaxis])
        return a / denominator


def normalize(x):
    if isinstance(x,dict):
        return normalize_dict_values(x)
    else:
        try:
            return x/sum(x)
        except TypeError:
            return [xi/sum(x) for xi in x]


def normalize_dict_values(d):
    return dict( zip(d.keys(), normalize(list(d.values())) ))


def multiply_diag(a, phi, copy=True):
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(df=a, cov_func=multiply_diag, phi=phi, copy=copy)
    else:
        if copy:
            b = np.copy(a)
            return multiply_diag(b, phi=phi, copy=False)
        else:
            n = np.shape(a)[0]
            for i in range(n):
                a[i, i] = a[i, i] * phi
            return a


def grand_mean(a):
    # np.trace(a)/n might be faster, haven't checked
    if isinstance(a,pd.DataFrame):
        return grand_mean(a.values)
    else:
        return np.mean(a.diagonal())


def grand_shrink(a, lmbd, copy=True):
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, grand_shrink, a=a, lmbd=lmbd)
    else:
        if copy:
            B = np.copy(a)
            return grand_shrink(B, lmbd=lmbd, copy=False)
        else:
            n = np.shape(a)[0]
            mu = grand_mean(a)
            return (1-lmbd) * a + lmbd * mu * np.eye(n)


def affine_inversion(a, phi=1.01, lmbd=0.01, copy=True):
    """ Combination of "ridge" (multiply diagonal) and "shrinkage" (towards mu*I)
    :param a:
    :param phi:
    :param lmbd:
    :return:
    """
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, affine_inversion, phi=phi, lmbd=lmbd)
    else:
        shrunk_cov = affine_shrink(a=a, phi=phi, lmbd=lmbd)
        try:
            pre = np.linalg.inv(shrunk_cov)
        except np.linalg.LinAlgError:
            pre = np.linalg.pinv(shrunk_cov)
        return pre


def affine_shrink(a, phi=1.01, lmbd=0.01, copy=True):
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, affine_shrink, phi=phi, lmbd=lmbd)
    else:
        ridge_cov = multiply_diag(a, phi=phi, copy=copy)
        shrunk_cov = grand_shrink(ridge_cov, lmbd=lmbd, copy=copy)
        return shrunk_cov


def is_symmetric(a, rtol=1e-05, atol=1e-08):
    if isinstance(a, pd.DataFrame):
        return is_symmetric(a.values, rtol=rtol, atol=atol)
    else:
        return np.allclose(a, a.T, rtol=rtol, atol=atol)


def to_symmetric(a):
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, to_symmetric)
    else:
        return (a + a.T) / 2.0


def dense_weights_from_dict(d:dict, shape=None, n_dim:int=None):
    """ Convert {1:3.141,0:123} -> [ 123, 3.141 ]
    :param d: Dictionary whose keys should be 0..n
    :param shape:
    :param n_dim:
    :return:
    """
    if shape is None:
        if n_dim is not None:
            shape = (n_dim,)
        else:
            n_dim = max(d.values())+1
    w = np.ndarray(shape=shape)
    for i in range(n_dim):
        w[i] = d[i]
    return w


def nearest_pos_def(a):
    """Find the nearest positive-definite matrix to input

    A Python/Numpy port of John D'Errico's `nearestSPD` MATLAB code [1], which
    credits [2].

    [1] https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd

    [2] N.J. Higham, "Computing a nearest symmetric positive semidefinite
    matrix" (1988): https://doi.org/10.1016/0024-3795(88)90223-6
    """
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, nearest_pos_def)
    else:
        b = to_symmetric(a)
        _, s, V = np.linalg.svd(b)
        H = np.dot(V.T, np.dot(np.diag(s), V))
        a2 = (b + H) / 2
        a3 = (a2 + a2.T) / 2

        if is_positive_def(a3):
            return a3

        spacing = np.spacing(np.linalg.norm(a))
        # The above is different from [1]. It appears that MATLAB's `chol` Cholesky
        # decomposition will accept matrixes with exactly 0-eigenvalue, whereas
        # Numpy's will not. So where [1] uses `eps(mineig)` (where `eps` is Matlab
        # for `np.spacing`), we use the above definition. CAVEAT: our `spacing`
        # will be much larger than [1]'s `eps(mineig)`, since `mineig` is usually on
        # the order of 1e-16, and `eps(1e-16)` is on the order of 1e-34, whereas
        # `spacing` will, for Gaussian random matrixes of small dimension, be on
        # othe order of 1e-16. In practice, both ways converge, as the unit test
        # below suggests.
        I = np.eye(a.shape[0])
        k = 1
        while not is_positive_def(a3):
            mineig = np.min(np.real(np.linalg.eigvals(a3)))
            a3 += I * (-mineig * k**2 + spacing)
            k += 1

        return a3


def is_positive_def(a):
    """Returns true when input is positive-definite, via Cholesky"""
    if isinstance(a,pd.DataFrame):
        return is_positive_def(a.values)
    else:
        try:
            _ = np.linalg.cholesky(a)
            return True
        except np.linalg.LinAlgError:
            return False


def make_diagonal(a):
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, make_diagonal)
    else:
        return np.diag(np.diag(a))


def mean_off_diag(a):
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, mean_off_diag)
    else:
        n = np.shape(a)[0]
        b = np.vectorize(int)(a)
        b = b - np.eye(n)
        the_sum = np.sum(b,axis=None)
        return the_sum/(n*(n-1))


def corr_distance(corr, expon=0.5):
    """
        Convert correlations into a distance between variables
    """
    if isinstance(corr, pd.DataFrame):
        return square_to_square_dataframe(corr, corr_distance, expon=expon)
    else:
        return ((1 - np.array(corr)) / 2.) ** expon


def cov_distance(cov, expon=0.5):
    """
           Convert covariance into a distance between variables
    """
    if isinstance(cov, pd.DataFrame):
        return square_to_square_dataframe(cov, cov_distance, expon=expon)
    else:
        corr = cov_to_corrcoef(cov)
        return corr_distance(corr=corr, expon=expon)


def try_invert(a, **affine_inversion_kwargs):
    """
       Attempt to invert a matrix by whatever means, falling back to ridge + shrinkage as required
    """
    if isinstance(a, pd.DataFrame):
        return square_to_square_dataframe(a, try_invert, **affine_inversion_kwargs)
    else:
        try:
            return np.linalg.inv(a)
        except np.linalg.LinAlgError:
            try:
                return np.linalg.pinv(a)
            except np.linalg.LinAlgError:
                return affine_inversion(a, **affine_inversion_kwargs)


def weaken_cov(cov, diag_multipliers:[float], off_diag_additional_factor=0.9):
    """  Augment a covariance matrix
    :param cov:
    :param diag_multipliers:             Vector to multiply diagonals by
    :param off_diag_additional_factor:   Additional multiplicative factor
    :return:
    """
    if isinstance(cov, pd.DataFrame):
        return square_to_square_dataframe(cov, weaken_cov, diag_multipliers=diag_multipliers, off_diag_additional_factor=off_diag_additional_factor)
    else:
        covs = np.copy(cov)
        for i, di in enumerate(diag_multipliers):
            covs[i, i] = covs[i, i] * di
            for j, dj in enumerate(diag_multipliers):
                if j != i:
                    covs[i, j] = off_diag_additional_factor * math.sqrt(di * dj) * covs[i, j]
        return covs


def approx_diag_of_inv(a):
    """
        Approximate diagonal entries of the inverse of a matrix
    """
    # TODO: https://cholmod-extra.readthedocs.io/en/latest/functions.html#sparse-inverse
    raise NotImplementedError


def bottom_schur_complement(A, B, C, D, gamma=1.0):
    # D - gamma C A^{-1} B
    return schur_complement(A=D, B=C, C=B, D=A, gamma=gamma)


def schur_complement(A,B,C,D, gamma=1.0):
    # A - gamma B D^{-1} C
    return _schur_complement_solve(A=A, B=B, C=C, D=D, gamma=gamma)


def _schur_complement_solve(A, B, C, D, gamma, warn=False, throw=False):
    # A - B D^{-1} C
    DinvC = inverse_multiply(a=D, b=C, warn=warn, throw=throw)
    M = A - gamma*np.dot( B, DinvC )

    CAREFUL = warn or throw
    if CAREFUL:
        rankD = np.linalg.matrix_rank(D)
        dimD = max(np.shape(D))
        if rankD==dimD:
            checkM = _schur_complement_pseudo(A=A,B=B,C=C,D=D, gamma=gamma)
            if not np.allclose( M, checkM ):
                print('schurly not')
        elif warn:
            print(' D is rank deficient, so schur complement is method dependent ')

    return M


def _schur_complement_pseudo(A, B, C, D, gamma):
    return A - gamma*np.dot( np.dot(B, np.linalg.pinv(D)),C)


def _schur_complement_direct(A, B, C, D, gamma):
    return A - gamma*np.dot( np.dot(B, np.linalg.pinv(D)),C)


def inverse_multiply(a, b, warn=False, throw=False):
    # Want  x = a^{-1} b
    #       a x = b
    #       x = solve(a,b)
    x = np.linalg.solve(a, b)
    if (warn or throw):
        if np.linalg.matrix_rank(x)<max(np.shape(a)):
            print('a is rank deficient so result is method dependent ')
        else:
            x_ = np.dot(np.linalg.inv(a), b)
            if not np.allclose(x_, x):
                if warn:
                    print('schurly not inverse multiply')
                if throw:
                    raise ValueError
    return x


def multiply_by_inverse(a, b, throw=True):
    #  Want x = a b^{-1}
    #       xt = bt^{-1} at  = inverse_multiply(bt, at)
    #       bt xt = at
    #       xt = solve(bt, at)
    if not np.allclose( np.shape(b)[1], np.shape(b)[0], np.shape(a)[1]):
        raise ValueError('dims wrong')
    bt = np.transpose(b)
    at = np.transpose(a)
    xt = np.linalg.solve(bt,at)
    x  = np.transpose(xt)
    x_check = np.dot(a, np.linalg.inv(b))
    if not np.allclose(x, x_check ) and throw:
        raise Exception('schurly not')
    return x


