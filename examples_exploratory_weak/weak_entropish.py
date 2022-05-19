from precise.skaters.managers.weakmanagers import weak_ewa_t0_d0_r050_n50_h500_long_manager as mgr
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
import numpy as np
from precise.skaters.portfoliostatic.weakportfactory import rel_entropish
from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r05 as f
from precise.skaters.portfoliostatic.allstaticport import LONG_PORT
from precise.skaters.covariance.runemp import run_emp_pcov_d0
from precise.skaters.locationutil.vectorfunctions import scatter

if __name__=='__main__':
    k = 1  # Business days
    n_dim = 100
    n_burn = 100
    rele = list()
    s_parity = {}
    w = None
    w_ports = None
    s_ports = [{} for _ in LONG_PORT]
    s_metric = {}
    s_contribution = {}

    while True:
        X = random_cached_equity_dense(k=k, n_dim=n_dim, n_obs=4000)
        s_mgr = {}
        s_cov = {}
        for y in X[:n_burn]:
            w, s_mgr = mgr(s=s_mgr, y=y)
            x_mean, x_cov, s_cov = f(y=y,s=s_cov,k=1)

        for i,y in enumerate(X[n_burn:]):
            if w is not None:
                realized_contribution = w * (np.dot(scatter(y), w))
                contrib_mean, contrib_var, s_contribution = run_emp_pcov_d0(y=realized_contribution,k=1, s=s_contribution)

                # Compare to contribution var for other portfolios
                w_ports = [port(cov=x_cov) for port in LONG_PORT ]
                realized_contributions = np.array([wp * (np.dot(scatter(y), wp)) for wp in w_ports])

                z_var = [np.var(realized_contribution)] + [np.var(zp) for zp in realized_contributions]
                z_mean, z_cov, s_metric = run_emp_pcov_d0(z_var, k=1, s=s_metric)
                if i % 3 == 1:
                    z_centered = [ zi/z_mean[0] for zi in z_mean]
                    LONG_PORT_NAMES = [str(pt).replace('_long_port','').replace('<function ','').replace('>','') for pt in LONG_PORT]
                    rankings = sorted(list(zip(z_centered[1:],LONG_PORT_NAMES)))
                    from pprint import pprint
                    pprint(rankings)

                if i % 5 == 1:
                    print(' ')
                    print('Contributions: ')
                    print( ','.join([str(c) for c in contrib_mean]) )
                    print((i,len(X)))

            x_mean, x_cov, s_cov = f(y=y, s=s_cov, k=1)
            w, s_mgr = mgr(s=s_mgr, y=y)





