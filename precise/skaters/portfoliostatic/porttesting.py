
from precise.skaters.portfolioutil.portcomparison import equity_portfolio_variance_rankings


def ports_test(ports, n_dim=10):
    """
          A quick crude way to test a slew of portfolio generation functions
    """
    return equity_portfolio_variance_rankings(ports, n_dim=n_dim)
