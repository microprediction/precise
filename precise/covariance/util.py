import numpy as np


def cov_to_corrcoef(cov):
    variances = np.diagonal(cov)
    denominator = np.sqrt(variances[np.newaxis, :] * variances[:, np.newaxis])
    return cov / denominator


def normalize(x):
    try:
        return x/sum(x)
    except:
        return [xi/sum(x) for xi in x]


def multiply_diag(A, phi, make_copy=True):
    if make_copy:
        B = np.copy(A)
        return multiply_diag(B, phi=phi, make_copy=False)
    else:
        n = np.shape(A)[0]
        for i in range(n):
            A[i,i] = A[i,i] * phi
        return A


def grand_shrink(A, lmbd, make_copy=True):
    if make_copy:
        B = np.copy(A)
        return grand_shrink(B, lmbd=lmbd, make_copy=False)
    else:
        n = np.shape(A)[0]
        mu = np.mean(A.diagonal())
        return (1-lmbd)*A + lmbd*mu*np.eye(n)
