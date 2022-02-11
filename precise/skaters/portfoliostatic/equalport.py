import numpy as np 
from precise.skaters.locationutil.vectorfunctions import normalize


def equal_long_port(cov=None, pre=None):
    """
      Equal weighted portfolio
    """
    if pre is not None:
        n_dim = np.shape(pre)[0]
    else:
        n_dim = np.shape(cov)[0]
    return np.array(normalize(np.ones(n_dim)))
    


EQUAL_LONG_PORT = [ equal_long_port ]
EQUAL_LS_PORT = []
EQUAL_PORT = EQUAL_LONG_PORT + EQUAL_LS_PORT