import numpy as np


def ecov_init(m:dict=None, x:[float]=None, n_dim=None):
    """ Empirical population covariance"""
    n_dim = len(x) if x is not None else n_dim
    if m is None:
      m = dict()
    m['n_dim']=n_dim
    m['shape']=(n_dim, n_dim)
    m['ones'] = np.ones(n_dim)
    m['count'] = 0
    m['mean'] = np.zeros(n_dim)
    m['pcov'] = np.zeros(m['shape'])
    return m

def ecov_update(m:dict, x:[float]):
    assert m['n_dim'] == len(x)
    m['count'] += 1
    delta = np.array(x - m['mean'])
    m['mean'] += delta / m['count']
    weighted_delta_at_n = np.array(x - m['mean']) / m['count']
    D_at_n = np.broadcast_to(weighted_delta_at_n, m['shape']).T
    I = np.identity(m['n_dim'])
    D = (delta * I).dot(D_at_n.T)
    m['pcov'] = m['pcov'] * (m['count'] - 1) / m['count'] + D
    return m


def merge_ecov(s:dict, other_s:dict):
    """ Merge two online covariance tracking objects as if the data had been merged """
    if other_s['n_dim'] != s['n_dim']:
        raise ValueError(
            f'''
               Cannot merge two OnlineCovariances with different orders.
               ({s['n_dim']} != {other_s['n_dim']})
               ''')

    merged_cov = ecov_init(n_dim=s['n_dim'])
    merged_cov['count'] = s['count'] + other_s['count']
    count_corr = (other_s['count'] * s['count']) / merged_cov['count']
    merged_cov['mean'] = (s['mean'] / other_s['count'] + other_s['mean'] / s['count']) * count_corr
    flat_mean_diff = s['mean'] - other_s['mean']
    mean_diffs = np.broadcast_to(flat_mean_diff, s['shape']).T
    merged_cov['pcov'] = (s['pcov'] * s['count']  + other_s['pcov'] * other_s['count'] + mean_diffs * mean_diffs.T * count_corr) / merged_cov['count']
    return merged_cov