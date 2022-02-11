from precise.skaters.portfoliostatic.schurportfactory import hierarchical_seriation_portfolio_factory

# HRP treated as special case of Schur


def hierarchical_risk_parity_portfolio_factory(seriator=None, alloc=None, port=None, splitter=None, cov=None, pre=None,
                                               n_split=5):
    port_kwargs = {}
    return hierarchical_seriation_portfolio_factory(seriator=seriator, port=port, splitter=splitter, port_kwargs=port_kwargs,
                                                    cov=cov, pre=pre, n_split=n_split)


