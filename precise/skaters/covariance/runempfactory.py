import numpy as np
from precise.skaters.covarianceutil.conventions import infer_dimension, X_DATA_TYPE, is_data


def emp_pcov(s:dict, x:[float]=None, n_dim=None, k=1)->dict:
    """
        Track empirical sample covariance
    """
    assert k==1
    if not s:
        s = _emp_pcov_init(x=x,n_dim=n_dim)
    if is_data(x):
        s = _emp_pcov_update(s=s, x=x)
    return s


def _emp_pcov_init(s:dict=None, x:X_DATA_TYPE=None, n_dim=None):
    """ Empirical population covariance"""
    n_dim = infer_dimension(x=x,n_dim=n_dim)
    if s is None:
       s = dict()
    s['n_dim']=n_dim
    s['shape']=(n_dim, n_dim)
    s['ones'] = np.ones(n_dim)
    s['n_samples'] = 0
    s['mean'] = np.zeros(n_dim)
    s['pcov'] = np.eye(n_dim)
    return s


def _emp_pcov_update(s:dict, x:X_DATA_TYPE, target=None):
    assert s['n_dim'] == len(x)
    prev_cov = np.copy( s['pcov'] )
    prev_mean = s['mean']
    s['n_samples'] += 1
    s['mean'] = prev_mean + (x - prev_mean)/s['n_samples']
    if target is None:
        delta_x_prev = np.atleast_2d(x-prev_mean)
        delta_x_current = np.atleast_2d(x - s['mean'])
    else:
        delta_x_prev = np.atleast_2d(x - target)
        delta_x_current = np.atleast_2d(x - target)
    s['pcov'] = prev_cov + ( np.matmul( delta_x_current.transpose(),delta_x_prev) - prev_cov ) / s['n_samples']

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