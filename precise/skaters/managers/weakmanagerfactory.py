from precise.skaters.managers.managerfactory import static_cov_manager_factory_d0
from precise.skaters.covariance.ewapm import ewa_pm_factory, ewa_pm_emp_scov_r01_n100
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.covariance.ewaempfactory import ewa_emp_pcov_factory
from functools import partial


def weak_pm_manager_factory(y, s, target, n_emp,r, a=1.0, b=None):
    """
       Weak portfolio construction using partial moments cov estimation
    """
    f = partial( ewa_pm_factory, k=1,r=r,target=target, n_emp=n_emp )
    port = partial( weak_portfolio_factory, a=a, b=b )
    return static_cov_manager_factory_d0(f=f, port=port, y=y, s=s)


def weak_ewa_manager_factory(y, s, n_emp, r , a=1.0, b=None):
    """
       Weak portfolio construction using partial moments cov estimation
    """
    f = partial( ewa_emp_pcov_factory, k=1,r=r, n_emp=n_emp )
    port = partial( weak_portfolio_factory, a=a, b=b )
    return static_cov_manager_factory_d0(f=f, port=port, y=y, s=s)
