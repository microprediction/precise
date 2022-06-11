import numpy as np
from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0
from precise.skaters.portfoliostatic.equalport import equal_long_port
from precise.skaters.covariance.identity import identity_scov
from precise.skaters.managers.buyandholdfactory import buy_and_hold_manager_factory


def equal_daily_long_manager(y, s, k=1, e=1, zeta=None, j=None):
    """ Trivial version ignored j argument """
    n_dim = len(y)
    w = np.ones(n_dim) / n_dim
    return w, {}


def equal_long_manager(y, s, k=1, e=1, zeta=None, j=1):
    """ Rebalance every j observations """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta, j=j)


def equal_weekly_long_manager(y, s, k=1, e=1, zeta=None, j=None):
    """ Rebalance every 5 observations, ignoring supplied j """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta, j=5)


def equal_weekly_buy_and_hold_long_manager(y, s, k=1, e=1, zeta=None, j=None):
    """ Rebalance every 5 observations, implemented a different way as a check for tests """
    return buy_and_hold_manager_factory(mgr=equal_daily_long_manager, j=5, y=y, s=s)


def equal_monthly_long_manager(y, s, k=1, e=1, zeta=None, j=None):
    """ Rebalance every 20 observations, ignoring supplied j """
    return static_cov_manager_factory_d0(y=y, s=s, f=identity_scov, port=equal_long_port, e=e, n_cold=0, zeta=zeta, j=20)




EQUAL_LONG_MANAGERS = [equal_long_manager, equal_daily_long_manager, equal_weekly_long_manager, equal_monthly_long_manager]
EQUAL_LS_MANAGERS = []
EQUAL_MANAGERS = EQUAL_LONG_MANAGERS + EQUAL_LS_MANAGERS
