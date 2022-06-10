import numpy as np
from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0
from precise.skaters.portfoliostatic.equalport import equal_long_port
from precise.skaters.covariance.identity import identity_scov
from precise.skaters.managers.buyandholdfactory import buy_and_hold_manager_factory


def equal_long_manager(y, s, k=1, e=1, zeta=None):
    n_dim = len(y)
    w = np.ones(n_dim) / n_dim
    return w, {}


def equal_long_manager_j5(y, s, k=1, e=1, zeta=None):
    """ Rebalance every 5 observations """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta, j=5)


def equal_long_manager_j5_verify(y, s, k=1, e=1, zeta=None):
    """ Rebalance every 5 observations, implemented a different way as a check """
    return buy_and_hold_manager_factory(mgr=equal_long_manager, j=5, y=y, s=s)


def equal_long_manager_j10(y, s, k=1, e=1, zeta=None):
    """ Rebalance every 5 observations """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta,
                                         j=10)


def equal_long_manager_j20(y, s, k=1, e=1, zeta=None):
    """ Rebalance every 5 observations """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta,
                                         j=20)


def equal_long_manager_j60(y, s, k=1, e=1, zeta=None):
    """ Rebalance every 5 observations """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta,
                                         j=60)


EQUAL_LONG_MANAGERS = [equal_long_manager, equal_long_manager_j5, equal_long_manager_j5_verify, equal_long_manager_j10,
                       equal_long_manager_j20, equal_long_manager_j60]
EQUAL_LS_MANAGERS = []
EQUAL_MANAGERS = EQUAL_LONG_MANAGERS + EQUAL_LS_MANAGERS
