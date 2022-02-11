from precise.skaters.managers.managerfactory import static_cov_manager_factory_d0
from precise.skaters.covariance.ewapm import ewa_pm_factory
from precise.skaters.portfoliostatic.schurportfactory import hierarchical_seriation_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.weakalloc import weak_allocation_factory
from precise.skaters.covariance.ewaempfactory import ewa_emp_pcov_factory
from functools import partial



def schur_weak_pm_manager_factory(y, s, target, n_emp, r, a=1.0, b=None, n_split=5, gamma=0.0, a_alloc=1.0, b_alloc=None):
    """
       HRP weak portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
           a_alloc, b_alloc - weak coefs used at parents
    """
    f = partial( ewa_pm_factory, k=1,r=r,target=target, n_emp=n_emp )
    alloc = partial( weak_allocation_factory, a=a_alloc, b=b_alloc )
    leaf_port = partial( weak_portfolio_factory, a=a, b=b )
    hrp_port = partial(hierarchical_seriation_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma)
    return static_cov_manager_factory_d0(f=f, port=hrp_port, y=y, s=s)


def hrp_weak_ewa_manager_factory(y, s, n_emp, r, a=1.0, b=None, n_split=5, gamma=0.0, a_alloc=1.0, b_alloc=None):
    """
       HRP weak portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
           a_alloc, b_alloc - weak coefs used at parents
    """
    f = partial( ewa_emp_pcov_factory, k=1,r=r, n_emp=n_emp )
    alloc = partial( weak_allocation_factory, a=a_alloc, b=b_alloc )
    leaf_port = partial( weak_portfolio_factory, a=a, b=b )
    hrp_port = partial(hierarchical_seriation_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma)
    return static_cov_manager_factory_d0(f=f, port=hrp_port, y=y, s=s)


