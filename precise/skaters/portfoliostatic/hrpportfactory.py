from precise.skaters.portfoliostatic.schurportfactory import hierarchical_seriation_portfolio_factory
import numpy as np


def hierarchical_risk_parity_portfolio_factory(seriator=None, alloc=None, port=None, splitter=None, cov=None, pre=None,
                                               n_split=5):
    return hierarchical_seriation_portfolio_factory(seriator=seriator, alloc=alloc, port=port, splitter=splitter,
                                                    cov=cov, pre=pre, n_split=n_split)


