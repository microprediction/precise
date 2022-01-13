from precise.covariance.movingaverage import ema_scov
from precise.covariance.matrixfunctions import grand_mean, grand_shrink
from sklearn.covariance._shrunk_covariance import ledoit_wolf_shrinkage
import numpy as np


# Experimental estimator inspired by Ledoit-Wolf
# Keeps a buffer of last n_buffer observations
# Tracks quantities akin to a^2, d^2 in LW


def lw_ema_scov(s:dict, x=None, r=0.025)->dict:
    if s.get('s_c') is None:
        if isinstance(x,int):
            return _lw_ema_scov_init(n_dim=x, r=r)
        else:
            s = _lw_ema_scov_init(n_dim=len(x), r=r)
    if x is not None:
        s = _lw_ema_scov_update(s=s, x=x, r=r)
    return s


def _lw_ema_scov_init(n_dim, r):
    sc = ema_scov({}, n_dim, r=r)
    return {'s_c':sc,
            'bn_bar':None,
            'a2':0,
            'mn':0,
            'n_new':0,
            'buffer':[]}


def _lw_ema_scov_update(s, x, r):
    """
        Attempts to track quantities similar to those used to estimate LD shrinkage
    """
    x = np.asarray(x)
    s['s_c']  = ema_scov(s=s['s_c'], x=x, r=r)
    s['buffer'].append(x)
    if len(s['buffer'])>s['s_c']['n_emp']:
        # Update running estimate of the LD shrinkage parameter
        s['n_new'] = s['n_new']+1
        xl = s['buffer'].pop(0)
        xc = np.atleast_2d(xl-s['s_c']['mean'])  # <--- Do we need this?
        scov = s['s_c']['scov']

        # Compute d^2
        mn = grand_mean(scov)
        s['mn'] = mn
        n_dim = np.shape(scov)[0]
        s['dn'] = np.linalg.norm(scov - mn * np.eye(n_dim))**2

        # Update b^2
        xc2 = xc
        xl2 = np.dot(xc2.T,xc2) - scov
        if s.get('bn_bar') is None:
            s['bn_bar'] = s['lmbd']*s['dn']
            s['lmbd_lw'] = 1.0 * s['lmbd']
        r_shrink = r/2 # <--- Heuristic
        bk = np.linalg.norm( xl2 )
        s['bn_bar'] = (1-r_shrink)*s['bn_bar'] + r_shrink*bk    # b^2
        ratio = bk/s['dn']

        # Imply new shrinkage
        bn = min( s['bn_bar'], s['dn'] )
        lmbd = bn/s['dn']
        s['lmbd'] = lmbd
    if 2< s['s_c']['n_samples']<2*s['s_c']['n_emp']:
        # Override with traditional Ledoit-Shrinkage
        X = np.asarray(s['buffer'])
        s['lmbd'] = ledoit_wolf_shrinkage(X=X)
    if s['s_c']['n_samples']>2:
        scov = s['s_c']['scov']
        s['scov'] = grand_shrink(a=scov, lmbd=s['lmbd'], copy=True)
    return s

















