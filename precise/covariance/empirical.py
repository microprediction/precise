import numpy as np


def _emp_pcov_init(s:dict=None, x:[float]=None, n_dim=None):
    """ Empirical population covariance"""
    n_dim = len(x) if x is not None else n_dim
    if s is None:
       s = dict()
    s['n_dim']=n_dim
    s['shape']=(n_dim, n_dim)
    s['ones'] = np.ones(n_dim)
    s['count'] = 0
    s['mean'] = np.zeros(n_dim)
    s['pcov'] = np.zeros(s['shape'])
    return s


def _emp_pcov_update(s:dict, x:[float]):
    assert s['n_dim'] == len(x)
    s['count'] += 1
    delta = np.array(x - s['mean'])
    s['mean'] += delta / s['count']
    weighted_delta_at_n = np.array(x - s['mean']) / s['count']
    D_at_n = np.broadcast_to(weighted_delta_at_n, s['shape']).T
    I = np.identity(s['n_dim'])
    D = (delta * I).dot(D_at_n.T)
    s['pcov'] = s['pcov'] * (s['count'] - 1) / s['count'] + D
    return s


def emp_pcov(s:dict, x:[float])->dict:
    """
        Track empirical sample covariance
    """
    if s.get('count') is None:
        if isinstance(x,int):
            return _emp_pcov_init(n_dim=x)
        else:
            return _emp_pcov_init(x=x)
    else:
        return _emp_pcov_update(s=s, x=x)


def merge_emp_scov(s:dict, other_s:dict):
    """ Merge two online covariance tracking objects as if the data had been merged """
    if other_s['n_dim'] != s['n_dim']:
        raise ValueError(
            f'''
               Cannot merge two OnlineCovariances with different orders.
               ({s['n_dim']} != {other_s['n_dim']})
               ''')

    merged_cov = _emp_pcov_init(n_dim=s['n_dim'])
    merged_cov['count'] = s['count'] + other_s['count']
    count_corr = (other_s['count'] * s['count']) / merged_cov['count']
    merged_cov['mean'] = (s['mean'] / other_s['count'] + other_s['mean'] / s['count']) * count_corr
    flat_mean_diff = s['mean'] - other_s['mean']
    mean_diffs = np.broadcast_to(flat_mean_diff, s['shape']).T
    merged_cov['pcov'] = (s['pcov'] * s['count']  + other_s['pcov'] * other_s['count'] + mean_diffs * mean_diffs.T * count_corr) / merged_cov['count']
    return merged_cov