import numpy as np
import pandas as pd
import precise
import NNS
from NNS.Partial_Moments import PM_matrix

def _NNS_pcov_init(s:dict=None, x:[[float]]=None, n_dim=None):
    """ NNS population covariancecomparisonutil"""
    n_dim = len(x[-1]) if x is not None else n_dim
    if s is None:
       s = dict()
    s['n_dim']=n_dim
    s['shape']=(n_dim, n_dim)
    s['ones'] = np.ones(n_dim)
    s['n_samples'] = 0
    s['pcov'] = np.zeros(s['shape'])
    return s


def _NNS_pcov_update(s:dict, x:[[float]]):
    assert s['n_dim'] == len(x[-1])
    s['n_samples'] += 1
    s['pcov'] = np.array(NNS.Partial_Moments.PM_matrix(1,1,s['n_dim']*[0],x, pop_adj=0)['cov.matrix'])
    return s


def NNS_pcov(s:dict, x:[[float]])->dict:
    """
        Track NNS sample covariancecomparisonutil
    """
    if s.get('n_samples') is None:
        if isinstance(x,int):
            return _NNS_pcov_init(n_dim=x)
        else:
            return _NNS_pcov_init(x=x)
    else:
        return _NNS_pcov_update(s=s, x=x)


def merge_NNS_scov(s:dict, other_s:dict):
    """ Merge two online covariancecomparisonutil tracking objects as if the data had been merged """
    if other_s['n_dim'] != s['n_dim']:
        raise ValueError(
            f'''
               Cannot merge two OnlineCovariances with different orders.
               ({s['n_dim']} != {other_s['n_dim']})
               ''')

    merged_cov = _NNS_pcov_init(n_dim=s['n_dim'])
    merged_cov['n_samples'] = s['n_samples'] + other_s['n_samples']
    count_corr = (other_s['n_samples'] * s['n_samples']) / merged_cov['n_samples']
    merged_cov['mean'] = (s['mean'] / other_s['n_samples'] + other_s['mean'] / s['n_samples']) * count_corr
    flat_mean_diff = s['mean'] - other_s['mean']
    mean_diffs = np.broadcast_to(flat_mean_diff, s['shape']).T
    merged_cov['pcov'] = (s['pcov'] * s['n_samples']  + other_s['pcov'] * other_s['n_samples'] + mean_diffs * mean_diffs.T * count_corr) / merged_cov['n_samples']
    return merged_cov