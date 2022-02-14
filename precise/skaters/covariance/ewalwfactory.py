from precise.skaters.covariance.ewaempfactory import ema_scov
from precise.skaters.covarianceutil.covfunctions import grand_mean, grand_shrink
from sklearn.covariance._shrunk_covariance import ledoit_wolf_shrinkage
import numpy as np


# EWALD short for "Exp Weight Avg" Ledoit-Wolf 
# ---------------------------------------------
# Experimental online estimator inspired by Ledoit-Wolf
# Keeps a buffer of last n_buffer observations
# Tracks quantities somewhat akin to a^2, d^2 used by LW to
# estimate a "reasonable" linear shrinkage


def ewa_lw_scov_factory(s, y, r, e=1):
    s = lw_ema_scov(s=s,x=y,r=r)
    x = np.copy(s['ema_scov']['mean'])
    x_cov = np.copy(s['scov'])
    return x, x_cov, s


def lw_ema_scov(s:dict, x=None, r=0.025)->dict:
    if s.get('ema_scov') is None:
        if isinstance(x,int):
            return _lw_ema_scov_init(n_dim=x, r=r)
        else:
            s = _lw_ema_scov_init(n_dim=len(x), r=r)
    if x is not None:
        s = _lw_ema_scov_update(s=s, x=x, r=r)
    return s


def _lw_ema_scov_init(n_dim, r):
    sc = ema_scov({}, n_dim, r=r)
    return {'ema_scov':sc,
            'bn_bar':None,
            'a2':0,
            'mn':0,
            'n_new':0,
            'buffer':[]}


def _lw_ema_scov_update(s, x, r):
    """
        Attempts to track quantities similar to those used to estimate LD shrinkage
    """
    # Uses buffered LD up to 2*n_emp observations, then switches to an updating scheme
    x = np.asarray(x)
    s['ema_scov']  = ema_scov(s=s['ema_scov'], x=x, r=r)
    s['buffer'].append(x)
    if len(s['buffer'])>s['ema_scov']['n_emp']:
        # Update running estimate of the LD shrinkage parameter
        s['n_new'] = s['n_new']+1
        xl = s['buffer'].pop(0)
        xc = np.atleast_2d(xl-s['ema_scov']['mean'])  # <--- Do we need this?
        scov = s['ema_scov']['scov']

        # Compute d^2
        mn = grand_mean(scov)
        s['mn'] = mn
        n_dim = np.shape(scov)[0]
        s['dn'] = np.linalg.norm((scov - mn * np.eye(n_dim))**2)

        # Update b^2
        xc2 = xc**2
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

    # If still warming up, override lmbd with traditional Ledoit-Shrinkage
    if 2 < s['ema_scov']['n_samples'] < 2*s['ema_scov']['n_emp']:
        X = np.asarray(s['buffer'])
        s['lmbd'] = ledoit_wolf_shrinkage(X=X)

    # Create shrunk version of moving avg sample covariance
    if s['ema_scov']['n_samples']>2:
        scov = s['ema_scov']['scov']
        s['scov'] = grand_shrink(a=scov, lmbd=s['lmbd'], copy=True)
    else:
        s['scov'] = np.eye(len(x))

    return s

















