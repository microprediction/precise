
import numpy as np


def identity_scov(s, y, k=1, e=1):
    """ Useful when you don't want to waste compute """
    # See equal_managers for usage example
    n_dim = len(y)
    return np.zeros(n_dim), np.eye(n_dim), s
