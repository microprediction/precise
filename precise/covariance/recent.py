import numpy as np
from precise.covariance.empirical import cov_init, cov_update

def rcov_init(n_dim=None, rho:float=0.05, n_cold=10):
    """ Initialize object to track exp moving avg cov"""
    s = cov_init(n_dim=n_dim)
    s.update({'rho':rho,'n_cold':n_cold})
    return s

def rcov_update(m:dict, x:[float], rho:float=None):
    """ Update recency weighted estimate of cov """
    if m['count']< m['n_cold']:
        # Use the regular cov update for a burn-in period
        m = cov_update(m=m, x=x)
        m['cov'] = m['pcov']*(m['count']-1)/m['count']
    else:
        m['count']+=1
        rho = m['rho'] if rho is None else rho
        assert m['n_dim'] == len(x)
        ycol = np.ndarray(shape=(m['n_dim'],1))
        ycol[:,0] = x - m['mean']
        yyt = np.dot(ycol, ycol.T)
        m['cov'] = (1 - rho) * m['cov'] + rho * yyt
        m['mean'] = (1 - rho) * m['mean'] + rho * x
    return m

