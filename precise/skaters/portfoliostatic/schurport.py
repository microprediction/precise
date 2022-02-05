from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
from precise.skaters.portfoliostatic.hrpportfactory import risk_parity_portfolio_factory


# Schur complement portfolios 


def schur_unit_s5_g1_port(cov=None, pre=None):
    return risk_parity_portfolio_factory(port=unit_portfolio_factory, cov=cov, pre=pre, n_split=5, gamma=1.0)


def schur_weak_s5_g1_long_port(cov=None, pre=None):
    return risk_parity_portfolio_factory(port=weak_portfolio_factory, cov=cov, pre=pre, n_split=5, gamma=1.0)


def schur_diag_s5_g1_long_port(cov=None, pre=None):
    return risk_parity_portfolio_factory(port=diagonal_portfolio_factory, cov=cov, pre=pre, n_split=5, gamma=1.0)



SCHUR_LONG_PORT = [ schur_diag_s5_g1_long_port,  schur_weak_s5_g1_long_port ]
SCHUR_LS_PORT = [ schur_unit_s5_g1_port ]
SCHUR_PORT = SCHUR_LONG_PORT + SCHUR_LS_PORT



if __name__=='__main__':
    from precise.skaters.portfolioutil.portcomparison import equity_portfolio_variance_rankings
    from pprint import pprint
    rankings = equity_portfolio_variance_rankings(ports=SCHUR_PORT, n_dim=60)
    pprint(rankings)