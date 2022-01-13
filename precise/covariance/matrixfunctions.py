import numpy as np


def cov_to_corrcoef(a):
    variances = np.diagonal(a)
    denominator = np.sqrt(variances[np.newaxis, :] * variances[:, np.newaxis])
    return a / denominator


def normalize(x):
    """ Normalize vector """
    try:
        return x/sum(x)
    except:
        return [xi/sum(x) for xi in x]


def multiply_diag(a, phi, copy=True):
    if copy:
        b = np.copy(a)
        return multiply_diag(b, phi=phi, copy=False)
    else:
        n = np.shape(a)[0]
        for i in range(n):
            a[i, i] = a[i, i] * phi
        return a


def grand_mean(a):
    # tr(a)/n
    return np.mean(a.diagonal())


def grand_shrink(a, lmbd, copy=True):
    if copy:
        B = np.copy(a)
        return grand_shrink(B, lmbd=lmbd, copy=False)
    else:
        n = np.shape(a)[0]
        mu = grand_mean(a)
        return (1-lmbd) * a + lmbd * mu * np.eye(n)


def is_symmetric(a, rtol=1e-05, atol=1e-08):
    return np.allclose(a, a.T, rtol=rtol, atol=atol)


def make_symmetric(a):
    return (a + a.T) / 2.0


def dense_weights_from_dict(d:dict, shape=None, n_dim:int=None):
    if shape is None:
        assert n_dim is not None, 'Cannot infer dimension'
        shape = (n_dim,)
    w = np.ndarray(shape=shape)
    for i in range(n_dim):
        w[i] = d[i]
    return w


from numpy import linalg as la


def nearest_pos_def(a):
    """Find the nearest positive-definite matrix to input

    A Python/Numpy port of John D'Errico's `nearestSPD` MATLAB code [1], which
    credits [2].

    [1] https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd

    [2] N.J. Higham, "Computing a nearest symmetric positive semidefinite
    matrix" (1988): https://doi.org/10.1016/0024-3795(88)90223-6
    """

    B = (a + a.T) / 2
    _, s, V = la.svd(B)
    H = np.dot(V.T, np.dot(np.diag(s), V))
    A2 = (B + H) / 2
    A3 = (A2 + A2.T) / 2

    if is_positive_def(A3):
        return A3

    spacing = np.spacing(la.norm(a))
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
    while not is_positive_def(A3):
        mineig = np.min(np.real(la.eigvals(A3)))
        A3 += I * (-mineig * k**2 + spacing)
        k += 1

    return A3


def is_positive_def(a):
    """Returns true when input is positive-definite, via Cholesky"""
    try:
        _ = la.cholesky(a)
        return True
    except la.LinAlgError:
        return False


def make_diagnonal(a):
    return np.diag(np.diag(a))


def mean_off_diag(a):
    n = np.shape(a)[0]
    b = np.vectorize(int)(a)
    b = b - np.eye(n)
    the_sum = np.sum(a,axis=None)
    return the_sum/(n*(n-1))


