
from precise.skaters.portfolioutil.portcomparison import m6_equity_portfolio_correlation_rankings


def ports_test(ports, n_dim=10):
    """
          A quick crude way to test a slew of portfolio generation functions

          ports: List of portfolio generators
    """
    return m6_equity_portfolio_correlation_rankings(ports, n_dim=n_dim)
