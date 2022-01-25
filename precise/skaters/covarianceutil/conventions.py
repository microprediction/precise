from typing import Union
import numpy as np

X_TYPE = Union[list,np.ndarray,int]
X_DATA_TYPE = Union[list,np.ndarray]
Y_TYPE = X_TYPE
Y_DATA_TYPE = X_DATA_TYPE


def infer_dimension(n_dim:int=None, x:X_TYPE=None, **ignore)->int:
    """ Infer the number of variables
    :param n_dim:
    :param x:
    :return:
    """
    if n_dim is not None:
        return n_dim
    elif isinstance(x, int):
        return x
    elif len(x)>1:
        return len(x)
    else:
        raise ValueError('Ambiguity in number of variables. Try supplying x or n_dim')


def is_data(x):
    return isinstance(x,np.ndarray) or isinstance(x,list)