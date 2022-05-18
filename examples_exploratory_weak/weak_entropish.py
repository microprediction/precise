from precise.skaters.managers.weakmanagers import weak_ewa_t0_d0_r050_n50_h500_long_manager as mgr
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
import numpy as np
from precise.skaters.portfoliostatic.weakportfactory import rel_entropish
from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r05 as f


if __name__=='__main__':
    k = 5  # Business days
    n_dim = 50
    X = random_cached_equity_dense(k=k, n_dim=n_dim, n_obs=120)
    np.shape(X)
    n_burn = 100
    s_mgr = {}  # Manager state

    s_cov = {}
    for y in X[:n_burn]:
        w, s_mgr = mgr(s=s_mgr, y=y)
        x_mean, x_cov, s_cov = f(y=y,s=s_cov,k=1)

    # After warming up...
    rele = list()
    for y in X[n_burn:]:
        x_mean, x_cov, s_cov = f(y=y, s=s_cov, k=1)
        w, s_mgr = mgr(s=s_mgr, y=y)
        rele.append(rel_entropish(w))

    print(rele)


