from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0
from precise.skaters.covariance.ewapm import ewa_pm_factory
from precise.skaters.covariance.bufempfactory import buf_emp_pcov_d0_factory
from precise.skaters.portfoliostatic.schurportfactory import schur_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.weakalloc import weak_allocation_factory
from precise.skaters.portfoliostatic.diagalloc import diagonal_allocation_factory
from precise.skaters.portfoliostatic.diagport import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.volalloc import vol_allocation_factory
from precise.skaters.portfoliostatic.ppoportfactory import ppo_vol_port
from precise.skaters.covariance.ewaempfactory import ewa_emp_pcov_factory
from precise.skaters.portfoliostatic.equalport import equal_long_port
from functools import partial



# Convenience functions for Schur managers
# These use either EWA cov estimation or partial moments, but more could be added


# Partial moments cov estimation


def schur_weak_weak_pm_manager_factory(y, s, target, n_emp, e, r, a=1.0, b=None, n_split=5, gamma=0, delta=0, zeta=0, a_alloc=1.0, b_alloc=None):
    """
       HRP weak portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
           a_alloc, b_alloc - weak coefs used at parents
    """
    f = partial( ewa_pm_factory, k=1, r=r,target=target, n_emp=n_emp )
    alloc = partial( weak_allocation_factory, a=a_alloc, b=b_alloc )
    leaf_port = partial( weak_portfolio_factory, a=a, b=b )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_diag_weak_pm_manager_factory(y, s, target, n_emp, e, r, a=1.0, b=None,  n_split=5, gamma=0.0,delta =0.0, zeta=0):
    """
       Schur with diag allocation and weak portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial( ewa_pm_factory, k=1, r=r,target=target, n_emp=n_emp )
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( weak_portfolio_factory, a=a, b=b )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_diag_equal_pm_manager_factory(y, s, target, n_emp, e, r, n_split=5, gamma=0.0, delta =0.0, zeta=0):
    """
       Schur with diag allocation and equal portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial( ewa_pm_factory, k=1, r=r,target=target, n_emp=n_emp )
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( equal_long_port )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_diag_vol_pm_manager_factory(y, s, target, n_emp, e, r, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with diag allocation and min-vol portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial( ewa_pm_factory, k=1, r=r,target=target, n_emp=n_emp )
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( ppo_vol_port )
    sch_port = partial( schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)



def schur_diag_diag_pm_manager_factory(y, s, target, n_emp, e, r, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with diag allocation and diag portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial( ewa_pm_factory, k=1, r=r,target=target, n_emp=n_emp )
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( diagonal_portfolio_factory )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_diag_diag_buf_emp_manager_factory(y, s, target, n_buffer, e, r, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with diag allocation and diag portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial( buf_emp_pcov_d0_factory, k=1, r=r,target=target, n_buffer=n_buffer )
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( diagonal_portfolio_factory )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_weak_diag_pm_manager_factory(y, s, target, n_emp, e, r, n_split=5, a=1.0, b=None, gamma=0.0, delta=0, zeta=0):
    """
       Schur with weak allocation and diag portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial( ewa_pm_factory, k=1, r=r,target=target, n_emp=n_emp )
    alloc = partial( weak_allocation_factory,  a=a, b=b )
    leaf_port = partial( diagonal_portfolio_factory )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


# EWA covariance estimation


def schur_weak_weak_ewa_manager_factory(y, s, n_emp, e, r, a=1.0, b=None, n_split=5, gamma=0.0, delta=0.0, a_alloc=1.0, b_alloc=None):
    """
       Schur weak allocation, weak portfolio construction, using partial moments cov estimation
           a, b             - weak coefs used at leaf
           a_alloc, b_alloc - weak coefs used at parents
    """
    f = partial( ewa_emp_pcov_factory, k=1,r=r, n_emp=n_emp )
    alloc = partial( weak_allocation_factory, a=a_alloc, b=b_alloc )
    leaf_port = partial( weak_portfolio_factory, a=a, b=b )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, s=s, y=y, e=e)


def schur_diag_weak_ewa_manager_factory(y, s, n_emp, e, r, a=1.0, b=None, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with diag allocation and weak portfolio construction using expon weighted cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial(ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp)
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( weak_portfolio_factory, a=a, b=b )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_diag_diag_ewa_manager_factory(y, s, n_emp, e, r, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with diag allocation and diag portfolio construction using expon weighted cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial(ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp)
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( diagonal_portfolio_factory )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)



def schur_diag_equal_ewa_manager_factory(y, s, n_emp, e, r, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with diag allocation and equal portfolio construction using partial moments cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial(ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp)
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( equal_long_port )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_weak_diag_ewa_manager_factory(y, s, n_emp, e, r, n_split=5, a=1.0, b=None, gamma=0.0, delta=0, zeta=0):
    """
       Schur with weak allocation and diag portfolio construction using expon weighted cov estimation
           a, b             - weak coefs used at leaf
           gamma=delta=0    - HRP
    """
    f = partial(ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp)
    alloc = partial( weak_allocation_factory,  a=a, b=b )
    leaf_port = partial( diagonal_portfolio_factory )
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_diag_vol_ewa_manager_factory(y, s, n_emp, e, r, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with diag allocation and min-vol portfolio construction  using expon weighted cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial(ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp)
    alloc = partial( diagonal_allocation_factory )
    leaf_port = partial( ppo_vol_port )
    sch_port = partial( schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_vol_vol_ewa_manager_factory(y, s, n_emp, e, r, n_split=5, gamma=0.0, delta=0, zeta=0):
    """
       Schur with vol allocation and min-vol portfolio construction  using expon weighted cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial(ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp)
    alloc = partial( vol_allocation_factory )
    leaf_port = partial( ppo_vol_port )
    sch_port = partial( schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)


def schur_weak_vol_ewa_manager_factory(y, s, n_emp, e, r, n_split=5, a=1.0, b=None, gamma=0.0, delta=0, zeta=0):
    """
       Schur with weak allocation and min-vol portfolio construction  using expon weighted cov estimation
           a, b             - weak coefs used at leaf
    """
    f = partial(ewa_emp_pcov_factory, k=1, r=r, n_emp=n_emp)
    alloc = partial( weak_allocation_factory,a=a, b=b )
    leaf_port = partial( ppo_vol_port )
    sch_port = partial( schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta)

