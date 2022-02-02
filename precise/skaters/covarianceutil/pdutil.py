import pandas as pd
import numpy as np


def square_to_square_dataframe(df, cov_func, **cov_func_kwargs):
    """ Map square dataframe to square dataframe """
    return pd.DataFrame( index=df.index, columns=df.columns, data=cov_func(df.values, **cov_func_kwargs))


def square_to_column_series(df, cov_func, **cov_func_kwargs):
    """ Map square dataframe to Series indexed by columns """
    return pd.Series( index=df.columns, data=cov_func(df.values, **cov_func_kwargs) )


def square_to_index_series(df, cov_func, **cov_func_kwargs):
    """ Map square dataframe to Series indexed by index """
    return pd.Series( index=df.index, data=cov_func(df.values, **cov_func_kwargs) )


def data_to_square_dataframe(df, data_func, **data_func_kwargs):
    return pd.DataFrame( index=df.columns, columns=df.columns, data=data_func(df.values, **data_func_kwargs))




def dict_or_series_values(d):
    # Remark: https://stackoverflow.com/questions/835092/python-dictionary-are-keys-and-values-always-the-same-order
    if isinstance(d,dict):
        return np.array(list(d.values()))
    elif isinstance(d,pd.Series):
        return d.values


def dict_or_series_to_scalar(d, func, **dict_func_kwargs):
    x = dict_or_series_values(d)
    return dict(zip(d.keys(), func(x, **dict_func_kwargs)))


def _square_and_vector_values(a,w):
    """ Takes square and vector arguments, which might be dict/Series/DataFrame
        Assumes columns of a correspond to index of w
    :param a:
    :param w:
    :return: (a,b), (b,)
    """
    if isinstance(a,pd.DataFrame) and isinstance(w, (dict, pd.Series)):
        if isinstance(w, pd.Series):
            w = w.to_dict()
        assert set(w.values()) == set(a.columns)
        w_values = np.array([w[ky] for ky in list(a.columns)])
        a_values = a.values
    elif isinstance(a,pd.DataFrame) and isinstance( w, (dict, pd.Series)):
        raise ValueError('too dangerous')
    elif isinstance(a, pd.DataFrame) and not isinstance( w, (dict, pd.Series)):
        a_values = a.values
        w_values = np.array(w)
    elif ~isinstance(a, pd.DataFrame) and isinstance( w, (dict, pd.Series)):
        a_values = a
        try:
            w_values = w.values()
        except TypeError:
            w_values = w.values
    else:
        raise NotImplementedError()
    return a_values, w_values


def square_and_vector_to_scalar(a, w, func, **func_kwargs):
    """
    :param a:   np 2d array or square dataframe
    :param w:   1d array, list, dict or Series
    :param func:    (a,w, **func_kwards) -> list or 1d array
    :param func_kwargs:
    :return:
    """
    a_values, w_values = _square_and_vector_values(a=a,w=w)
    return func(a_values, w_values, **func_kwargs)


def square_and_vector_to_vector(a, w, func, **func_kwargs):
    """
    :param a:   np 2d array or square dataframe
    :param w:   1d array, list, dict or Series
    :param func:    (a,w, **func_kwards) -> list or 1d array
    :param func_kwargs:
    :return:
    """
    a_values, w_values = _square_and_vector_values(a=a, w=w)
    y_values = func( a_values, w_values, **func_kwargs)
    if isinstance(w, dict):
        return dict(zip( w.keys(), y_values))
    elif isinstance(w, pd.Series):
        return pd.Series(index=w.index, data=y_values)
    else:
        return np.array(y_values)


def vector_to_vector(w, func, **func_kwargs):
    if isinstance(w, dict):
        y_values = func( w.values(), **func_kwargs )
        return dict(zip(w.keys(),y_values))
    elif isinstance(w, pd.Series):
        y_values = func( w.values, **func_kwargs )
        return pd.Series(index=w.index, data=y_values)
    else:
        return func( np.array(w) )





