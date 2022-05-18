from precise.skaters.managers.weakmanagers import weak_ewa_t0_d0_r050_n50_h500_long_manager as mgr
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
import numpy as np
from precise.skaters.portfoliostatic.weakportfactory import rel_entropy
from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r05 as f


if __name__=='__main__':
    k = 1  # Business days
    n_dim = 20
    X = random_cached_equity_dense(k=k, n_dim=n_dim, n_obs=2000)
    np.shape(X)
    n_burn = 100
    s_mgr = {}  # Manager state
    s_cov = {}
    for y in X[:n_burn]:
        w, s_mgr = mgr(s=s_mgr, y=y)
        x_mean, x_cov, s_cov = f(y=y,s=s_cov,k=1)

    # After warming up...
    rele = list()
    from precise.skaters.covariance.runemp import run_emp_pcov_d0
    from precise.skaters.locationutil.vectorfunctions import scatter
    s_parity = {}
    w = None
    for y in X[n_burn:]:
        if w is not None:
            z = w*(np.dot( scatter(y), w ))
            w_eq = np.ones_like(w)
            z_eq = w_eq*(np.dot( scatter(y), w_eq ))
            z_std = [np.std(z), np.std(z_eq)]
            z_mean, z_cov, s_parity = run_emp_pcov_d0(z_std,k=1,s=s_parity)

        x_mean, x_cov, s_cov = f(y=y, s=s_cov, k=1)
        w, s_mgr = mgr(s=s_mgr, y=y)
        rele.append(rel_entropy(w))


    print(np.diag(z_cov))
    pass



