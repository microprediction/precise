import numpy as np


def equal_long_manager(y, s, k=1, e=1, zeta=None):
    n_dim = len(y)
    w = np.ones(n_dim)/n_dim
    return w, {}


EQUAL_LONG_MANAGERS = [equal_long_manager]
EQUAL_LS_MANAGERS = []
EQUAL_MANAGERS = EQUAL_LONG_MANAGERS + EQUAL_LS_MANAGERS
