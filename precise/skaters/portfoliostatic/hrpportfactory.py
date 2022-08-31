from precise.skaters.portfoliostatic.schurportfactory import schur_portfolio_factory

# A version of hierarchical risk parity


def hierarchical_risk_parity_portfolio_factory(cov=None, pre=None, port=None, port_kwargs=None,
                            alloc=None, alloc_kwargs=None,
                            n_split=5, delta=0.0, jiggle=True):
    """
        A special case of schur portfolio optimization with gamma=0.0
    """
    gamma = 0.0
    seriation_depth = 1
    return schur_portfolio_factory(cov=cov, pre=pre, port=port, port_kwargs=port_kwargs,
                                   alloc=alloc, alloc_kwargs=alloc_kwargs,
                                   n_split=n_split, gamma=gamma, delta=delta,
                                   jiggle=jiggle, seriation_depth=seriation_depth)


