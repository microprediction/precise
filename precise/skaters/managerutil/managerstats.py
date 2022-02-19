import time
import numpy as np
from momentum.functions import var_init, var_update
from itertools import zip_longest


def manager_info(contestant, xs, n_burn, **ignore):
    # evaluator for battles
    metrics = manager_stats(mgr=contestant, xs=xs, n_burn=n_burn)
    return metrics['info'], metrics


def manager_var(contestant, xs, n_burn, **ignore):
    # evaluator for battles
    metrics = manager_stats(mgr=contestant, xs=xs, n_burn=n_burn)
    return -metrics['var'], metrics


def manager_stats(mgr, xs, n_burn=10):
    """
       Compute manager stats.
       Sends e=-1 during burn-in, then e=1 during assessment period

       :returns  dict with  mean, var, kurtosis etc of portfolio returns
    """
    start_time = time.time()
    n_obs, n_dim = np.shape(xs)
    assert n_obs > n_burn

    s = {}     # Manager state

    print('     burning in')
    for y in xs[:n_burn]:
        w, s = mgr(s=s, y=y, k=1, e=-1)
    print('        burn in complete', flush=True)

    print('     evaluating')
    metrics = var_init()
    w_prev = None
    mrg_time = 0
    for m, y in enumerate(xs[n_burn:]):
        if w_prev is not None:
            x = sum( [ yi*wi for yi,wi in zip_longest( y,w_prev) ] )
            metrics = var_update(metrics, x=x)

        # Store portfolio for assessment against next data point
        w_prev = w

        # Make next portfolio selection
        st = time.time()
        w, s = mgr(s=s, y=y, k=1, e=1)
        mrg_time += time.time()-st

    total_time = time.time() - start_time
    metrics.update({'time':mrg_time,'total_time':total_time})
    metrics['info'] = metrics['mean']/metrics['std']
    print('     info = '+str(metrics['info']))
    print('     std  = ' + str(metrics['std']))
    return metrics


if __name__=='__main__':
    import random
    from precise.skaters.managers.allmanagers import LONG_MANAGERS
    xs = np.random.randn(500,3)
    for contestant in LONG_MANAGERS:
       print(contestant.__name__)
       ll, metrics = manager_info(contestant=contestant, xs=xs, n_burn=50)
       print('   '+str(ll))
