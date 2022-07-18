from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0
from precise.skaters.covariance.ewalwfactory import ewa_lw_scov_factory
from precise.skaters.portfoliostatic.schurportfactory import schur_portfolio_factory
from precise.skaters.portfoliostatic.volalloc import vol_allocation_factory
from precise.skaters.portfoliostatic.ppoportfactory import ppo_vol_port
from functools import partial


def molyboga_manager_factory(y, s, e, r, n_split=5, gamma=0.0, delta=0, zeta=0,j=1,q=1.0):
    """
       Schur with vol allocation and
                  min-vol portfolio construction
                  using expon weighted cov estimation
                  with LD shrinkage

           r                - decay used in LD cov estimation

           a, b             - weak coefs used at leaf

       https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3588908
       This paper introduces a Modified Hierarchical Risk Parity ("MHRP") approach that extends the HRP approach
        by incorporating three intuitive elements commonly used by practitioners. The new approach (i) replaces the
         sample covariance matrix with an exponentially weighted covariance matrix with Ledoit-Wolf shrinkage,
          (ii) improves diversification across portfolio constituents both within and across clusters by relying
           on an equal volatility, rather than an inverse variance, allocation approach, and (iii) improves
        diversification across time by applying volatility targeting to portfolios.

      (Note that this implementation generalizes on that of Marat Molyboga due to the optional introduction of Schur
      complements. Just set gamma=delta=0 for something close to the spirit of that paper).

    """
    f = partial(ewa_lw_scov_factory, k=1, r=r)
    alloc = partial( vol_allocation_factory )
    leaf_port = partial( ppo_vol_port )
    sch_port = partial( schur_portfolio_factory, alloc=alloc, port=leaf_port, n_split=n_split, gamma=gamma, delta=delta)
    return static_cov_manager_factory_d0(f=f, port=sch_port, y=y, s=s, e=e, zeta=zeta,j=j,q=q)
