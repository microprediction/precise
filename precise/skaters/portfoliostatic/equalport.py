import numpy as np 
from precise.skaters.locationutil.vectorfunctions import normalize
import pandas as pd


def equal_long_port(cov=None, pre=None, as_dense=False):
    """
      Equal weighted portfolio
      :param as_dense   If True, will always return np.array even if cov or pre
    """
    if pre is not None:
        n_dim = np.shape(pre)[0]
    else:
        n_dim = np.shape(cov)[0]
    w = np.array(normalize(np.ones(n_dim)))

    as_series = (not as_dense) and ((cov is not None) and isinstance(cov,pd.DataFrame)) or ((pre is not None) and isinstance(pre,pd.DataFrame))
    if as_series:
        return pd.Series(index=cov.columns, data=w)
    else:
        return w

    


EQUAL_LONG_PORT = [ equal_long_port ]
EQUAL_LS_PORT = []
EQUAL_PORT = EQUAL_LONG_PORT + EQUAL_LS_PORT