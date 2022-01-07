import numpy as np

# Minor adaptations to code by Carsten Schelp
# https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html


def online_empirical_cov(s:dict=None, y:[float]=None, n_dim=None):
    if s is None or s.get('n_dim') is None:
        n_dim = len(y) if y is not None else n_dim
        if s is None:
          s = dict()
        s['n_dim']=n_dim
        s['shape']=(n_dim,n_dim)
        s['identity'] = np.identity(n_dim)
        s['ones'] = np.ones(n_dim)
        s['count'] = 0
        s['mean'] = np.zeros(n_dim)
        s['cov'] = np.zeros(s['shape'])
    if y is not None:
        assert s['n_dim'] == len(y)
        s['count'] += 1
        delta_at_nMin1 = np.array(y - s['mean'])
        s['mean'] += delta_at_nMin1 / s['count']
        weighted_delta_at_n = np.array(y - s['mean']) / s['count']
        D_at_n = np.broadcast_to(weighted_delta_at_n, s['shape']).T
        D = (delta_at_nMin1 * s['identity']).dot(D_at_n.T)
        s['cov'] = s['cov'] * (s['count'] - 1) / s['count'] + D
    return s 


def merge_online_empirical_cov(s:dict, other_s:dict):
    """ Merge two online covariance tracking objects as if the data had been merged """
    if other_s['n_dim'] != s['n_dim']:
        raise ValueError(
            f'''
               Cannot merge two OnlineCovariances with different orders.
               ({s['n_dim']} != {other_s['n_dim']})
               ''')

    merged_cov = online_empirical_cov(n_dim=s['n_dim'])
    merged_cov['count'] = s['count'] + other_s['count']
    count_corr = (other_s['count'] * s['count']) / merged_cov['count']
    merged_cov['mean'] = (s['mean'] / other_s['count'] + other_s['mean'] / s['count']) * count_corr
    flat_mean_diff = s['mean'] - other_s['mean']
    mean_diffs = np.broadcast_to(flat_mean_diff, s['shape']).T
    merged_cov['cov'] = (s['cov'] * s['count']  + other_s['cov'] * other_s['count'] + mean_diffs * mean_diffs.T * count_corr) / merged_cov['count']
    return merged_cov