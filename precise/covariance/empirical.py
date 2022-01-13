import numpy as np


def _emp_pcov_init(s:dict=None, x:[float]=None, n_dim=None):
    """ Empirical population covariance"""
    n_dim = len(x) if x is not None else n_dim
    if s is None:
       s = dict()
    s['n_dim']=n_dim
    s['shape']=(n_dim, n_dim)
    s['ones'] = np.ones(n_dim)
    s['n_samples'] = 0
    s['mean'] = np.zeros(n_dim)
    s['pcov'] = np.zeros(s['shape'])
    return s


def _emp_pcov_update(s:dict, x:[float]):
    assert s['n_dim'] == len(x)
    s['n_samples'] += 1
    delta = np.array(x - s['mean'])
    s['mean'] += delta / s['n_samples']
    weighted_delta_at_n = np.array(x - s['mean']) / s['n_samples']
    D_at_n = np.broadcast_to(weighted_delta_at_n, s['shape']).T
    I = np.identity(s['n_dim'])
    D = (delta * I).dot(D_at_n.T)
    s['pcov'] = s['pcov'] * (s['n_samples'] - 1) / s['n_samples'] + D
    return s


def emp_pcov(s:dict, x:[float])->dict:
    """
        Track empirical sample covariance
    """
    if s.get('n_samples') is None:
        if isinstance(x,int):
            return _emp_pcov_init(n_dim=x)
        else:
            s = _emp_pcov_init(x=x)
    if len(x)>1:
        s= _emp_pcov_update(s=s, x=x)
    return s


def merge_emp_scov(s:dict, other_s:dict):
    """ Merge two online covariance tracking objects as if the data had been merged """
    if other_s['n_dim'] != s['n_dim']:
        raise ValueError(
            f'''
               Cannot merge two OnlineCovariances with different orders.
               ({s['n_dim']} != {other_s['n_dim']})
               ''')

    merged_cov = _emp_pcov_init(n_dim=s['n_dim'])
    merged_cov['n_samples'] = s['n_samples'] + other_s['n_samples']
    count_corr = (other_s['n_samples'] * s['n_samples']) / merged_cov['n_samples']
    merged_cov['mean'] = (s['mean'] / other_s['n_samples'] + other_s['mean'] / s['n_samples']) * count_corr
    flat_mean_diff = s['mean'] - other_s['mean']
    mean_diffs = np.broadcast_to(flat_mean_diff, s['shape']).T
    merged_cov['pcov'] = (s['pcov'] * s['n_samples']  + other_s['pcov'] * other_s['n_samples'] + mean_diffs * mean_diffs.T * count_corr) / merged_cov['n_samples']
    return merged_cov