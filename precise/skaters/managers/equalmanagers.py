import numpy as np
from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0
from precise.skaters.portfoliostatic.equalport import equal_long_port
from precise.skaters.covariance.identity import identity_scov
from precise.skaters.managers.buyandholdfactory import buy_and_hold_manager_factory

# Two different implementations of a manager that steers towards equal weighted portfolios


def equal_long_manager(y, s, k=1, e=1, zeta=None, j=1,q=1.0):
    """ Periodically sets all portfolio weights equal

           j   Recomputation frequency
           q   Fraction of new versus old

    """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta, j=j, q=q)


def equal_check_long_manager(y, s, k=1, e=1, zeta=None, j=1, q=1.0):
    """  Same as above but with a different implementation """
    return buy_and_hold_manager_factory(mgr=_equivalence_long_manager, j=j, q=q, y=y, s=s)


def _equivalence_long_manager(y, s, k=1, e=1, zeta=None, j=None, q=None):
    """  Always sets weight equal """
    n_dim = len(y)
    w = np.ones(n_dim) / n_dim
    return w, {}


EQUAL_LONG_MANAGERS = [equal_long_manager, equal_check_long_manager]
EQUAL_LS_MANAGERS = []
EQUAL_MANAGERS = EQUAL_LONG_MANAGERS + EQUAL_LS_MANAGERS
