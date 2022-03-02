from precise.skaters.portfoliostatic.unitport import unit_port
from precise.skaters.portfoliostatic.weakportfactory import optimal_b, weaken_cov
import numpy as np
from precise.skaters.portfolioutil.portfunctions import negative_mass, exclude_negative_weights



def max_discrepancy_from_e(e, n_dim):
    if e is None:
        e = 1.0
    if e > 0:
        r = 1 + e**2
        max_discrepancy = 1 / (r * n_dim)
    if abs(e) < 1e-6:
        max_discrepancy = 1 / n_dim
    if e < 0:
        max_discrepancy = 10000000
    return max_discrepancy


def weak_pcov_factory(y, f, s:dict, k=1, e=1, max_neg_mass=0.01, **f_kwargs):
    """
         Takes a covariance skater f and shrinks off-diagonal
         (A speculative method motivated by out of sample portfolio performance)
    """

    one_vec = np.ones_like(y)
    n_dim = len(y)
    w_equal = one_vec/n_dim
    d = np.ones(n_dim)
    if not s:
        s = {'s_f':{},
             'b':1.0,
             'w':w_equal}
    x_mean, x_cov, s['s_f'] = f(y=y, s=s['s_f'], k=k, e=e, **f_kwargs)

    # Shrink off-diagonal cov entries and check that the resultant portfolio hasn't changed too much
    weak_cov = weaken_cov(cov=x_cov,diag_multipliers=d, off_diag_additional_factor=s['b'] )
    max_discrepancy = max_discrepancy_from_e(e=e,n_dim=n_dim)
    discrep = np.linalg.norm( np.dot(weak_cov,s['w']) - one_vec )
    if discrep > max_discrepancy:  # <-- what should this be?
        # Update the shrinkage parameter b, and the weak portfolio
        w_min_var = unit_port(cov=x_cov)
        neg_mass = negative_mass(w_min_var)
        if neg_mass > max_neg_mass:
             b = optimal_b(cov=x_cov, w0=w_min_var)
             d = np.ones(n_dim)
             x_cov = weaken_cov(cov=x_cov, diag_multipliers=d, off_diag_additional_factor=b)
             w = unit_port(cov=x_cov)
             s['b'] = b
             s['w'] = w
    return x_mean, weak_cov, s

