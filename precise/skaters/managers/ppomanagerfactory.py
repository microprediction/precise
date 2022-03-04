from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0
from precise.skaters.covariance.ewapm import ewa_pm_factory, ewa_pm_emp_scov_r01_n100
from precise.skaters.portfoliostatic.ppoportfactory import ppo_portfolio_factory, PPO_LONG_BOUNDS
from precise.skaters.covariance.ewaempfactory import ewa_emp_pcov_factory
from functools import partial


def ppo_long_manager_factory(y,s, f, method, e=1, zeta=0):
    port = partial(ppo_portfolio_factory, method=method, as_dense=True, weight_bounds=PPO_LONG_BOUNDS)
    return static_cov_manager_factory_d0(f=f, port=port, y=y, s=s, e=e, zeta=zeta)


def ppo_pm_long_manager_factory(y, s, method, target, n_emp, r, e=1, zeta=0):
    """
       PyPortfolioOpt portfolio construction using partial moments cov estimation
    """
    f = partial( ewa_pm_factory, k=1,r=r,target=target, n_emp=n_emp )
    port = partial( ppo_portfolio_factory, method=method, as_dense=True, weight_bounds=PPO_LONG_BOUNDS )
    return static_cov_manager_factory_d0(f=f, port=port, y=y, s=s, e=e, zeta=zeta)


def ppo_ewa_long_manager_factory(y, s, method, n_emp, r, e=1, zeta=0):
    """
       PyPortfolioOpt portfolio construction using EWA cov estimation
    """
    f = partial( ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp )
    port = partial( ppo_portfolio_factory, method=method, as_dense=True, weight_bounds=PPO_LONG_BOUNDS )
    return static_cov_manager_factory_d0(f=f, port=port, y=y, s=s, e=e, zeta=zeta)

