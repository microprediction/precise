from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
from precise.skaters.portfoliostatic.hrpportfactory import risk_parity_portfolio_factory


# Hierarchical Risk-Parity


def hrp_unit_s5_port(cov=None, pre=None):
    return risk_parity_portfolio_factory(port=unit_portfolio_factory, cov=cov, pre=pre, n_split=5)


def hrp_weak_s5_long_port(cov=None, pre=None):
    return risk_parity_portfolio_factory(port=weak_portfolio_factory, cov=cov, pre=pre, n_split=5)


def hrp_diag_s5_long_port(cov=None, pre=None):
    return risk_parity_portfolio_factory(port=diagonal_portfolio_factory, cov=cov, pre=pre, n_split=5)



HRP_LONG_PORT = [hrp_weak_s5_long_port, hrp_diag_s5_long_port]
HRP_LS_PORT = [ hrp_unit_s5_port ]
HRP_PORT = HRP_LONG_PORT + HRP_LS_PORT



if __name__=='__main__':
    from precise.skaters.portfolioutil.portcomparison import equity_portfolio_variance_rankings
    from pprint import pprint
    rankings = equity_portfolio_variance_rankings(ports=HRP_PORT, n_dim=60)
    pprint(rankings)