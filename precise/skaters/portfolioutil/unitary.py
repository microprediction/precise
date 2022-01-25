import numpy as np
from precise.skaters.locationutil import normalize

# sum(w)=1

def unitary_from_pre(pre):
    """ Min var portfolio summing to unity """
    # No optimization required
    n_dim = np.shape(pre)[1]
    wones = np.ones(shape=(n_dim, 1))
    return normalize(np.squeeze(np.matmul(pre, wones)))


def unitary_from_cov(cov):
    try:
        pre = np.linalg.inv(cov)
    except:
        pre = np.linalg.pinv(cov)
    return unitary_from_pre(pre)