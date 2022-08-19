from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0
from precise.skaters.covariance.ewalwfactory import ewa_lw_scov_factory
from precise.skaters.portfoliostatic.schurportfactory import schur_portfolio_factory
from precise.skaters.portfoliostatic.weakalloc import weak_allocation_factory
from precise.skaters.portfoliostatic.volalloc import vol_allocation_factory
from precise.skaters.portfoliostatic.rpportfactory import rp_portfolio_factory
from functools import partial


def slurp_vol_manager_factory(y, s, e, r, n_split=5, phi=1.0,gamma=0.0, delta=0, zeta=0,j=1,q=1.0):
    """  A sluring of "Schur Ledoit Risk Parity"

            Weak allocation,
            RP portfolio with shrinkage phi

    """
    f = partial(ewa_lw_scov_factory, k=1, r=r)
    alloc = partial( vol_allocation_factory )
    leaf_port = partial( rp_portfolio_factory, phi=phi )
    sch_port = partial( schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta,j=j,q=q)


def slurp_weak_manager_factory(y, s, e, r, n_split=5, phi=1.0, gamma=0.0, delta=0, zeta=0, j=1, q=1.0):
    """  A sluring of "Schur Ledoit Risk Parity"

    """
    f = partial(ewa_lw_scov_factory, k=1, r=r)
    alloc = partial(weak_allocation_factory)
    leaf_port = partial(rp_portfolio_factory, phi=phi)
    sch_port = partial(schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta, j=j, q=q)
