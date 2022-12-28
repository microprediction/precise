import time
import numpy as np
from momentum.functions import var_init, var_update
from itertools import zip_longest
from pprint import pprint


def manager_info(contestant, xs, n_burn, **ignore):
    # evaluator for battles
    metrics = manager_stats(mgr=contestant, xs=xs, n_burn=n_burn)
    return metrics['info'], metrics


def manager_var(contestant, xs, n_burn, **ignore):
    # evaluator for battles
    metrics = manager_stats(mgr=contestant, xs=xs, n_burn=n_burn)
    return -metrics['var'], metrics


def var_metric(y,w_prev):
    return sum([yi * wi for yi, wi in zip_longest(y, w_prev)])


def manager_stats_leaderboard(mgrs, xs, n_burn=100, metric=var_metric, j=1, q=1.0, verbose=True, field='info'):
    """
    :param mgrs:
    :param xs:
    :param n_burn:
    :param metric:
    :param j:
    :param q:
    :param verbose:
    :param field:
    :return:  [ (score, name, manager) ]
    """
    lb = list()
    for mgr in mgrs:
        stats = manager_stats(mgr=mgr, xs=xs, n_burn=n_burn, j=j, q=q, metric=metric, verbose=False)
        score = stats[field]
        lb.append((score, mgr.__name__, mgr))
        info_brief = [(s, n) for (s, n, _) in lb]
        if verbose:
            pprint(sorted(info_brief, reverse=True))
    return lb


def manager_stats(mgr, xs, n_burn=100, metric=var_metric, j=1, q=1.0, verbose=False):
    """
       Compute manager stats.
       Sends e=-1 during burn-in, then e=1 during assessment period
       :returns  dict with  mean, var, kurtosis etc of portfolio returns
    """
    start_time = time.time()
    n_obs, n_dim = np.shape(xs)
    assert n_obs > n_burn

    s = {}  # Manager state

    if verbose:
      print('     burning in')
    for y in xs[:n_burn]:
        w, s = mgr(s=s, y=y, k=1, e=-1, j=j, q=q)

    if verbose:
        print('        burn in complete', flush=True)

    # print('     evaluating')
    metrics = var_init()
    w_prev = None
    mrg_time = 0
    for m, y in enumerate(xs[n_burn:]):
        if w_prev is not None:
            x = metric(y=y, w_prev=w_prev)
            metrics = var_update(metrics, x=x)

        # Store portfolio for assessment against next data point
        w_prev = w

        # Make next portfolio selection
        st = time.time()
        w, s = mgr(s=s, y=y, k=1, e=1, j=j, q=q)
        mrg_time += time.time() - st

    total_time = time.time() - start_time
    metrics.update({'time': mrg_time, 'total_time': total_time})
    metrics['info'] = metrics['mean'] / metrics['std']
    if verbose:
        print('   sharpe = ' + str(metrics['info']))
        print('     std  = ' + str(metrics['std']))
        print(' last weight = ' + str(w))
    return metrics


if __name__=='__main__':
    import random
    from precise.skaters.managers.allmanagers import LONG_MANAGERS
    xs = np.random.randn(500,3)
    for contestant in LONG_MANAGERS:
       print(contestant.__name__)
       ll, metrics = manager_info(contestant=contestant, xs=xs, n_burn=50)
       print('   '+str(ll))
