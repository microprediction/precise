from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
from precise.skaters.portfoliostatic.hrpportfactory import hierarchical_risk_parity_portfolio_factory
from precise.skaters.portfoliostatic.diagalloc import diag_alloc
from precise.skaters.portfoliostatic.unitalloc import unit_alloc
from precise.skaters.portfoliostatic.weakalloc import weak_long_alloc


# Hierarchical Risk-Parity


def hrp_diag_diag_s5_long_port(cov=None, pre=None):
    # Lopez de Prado 2016
    # Allocate using diagonal
    return hierarchical_risk_parity_portfolio_factory(port=diagonal_portfolio_factory, alloc=diag_alloc, cov=cov, pre=pre, n_split=5)


def hrp_unit_unit_s5_port(cov=None, pre=None):
    return hierarchical_risk_parity_portfolio_factory(port=unit_portfolio_factory, alloc=unit_alloc, cov=cov, pre=pre, n_split=5)


def hrp_weak_weak_s5_long_port(cov=None, pre=None):
    return hierarchical_risk_parity_portfolio_factory(port=weak_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5)


# Weak allocation ...

def hrp_unit_weak_s5_port(cov=None, pre=None):
    return hierarchical_risk_parity_portfolio_factory(port=unit_portfolio_factory, alloc=unit_alloc, cov=cov, pre=pre, n_split=5)


def hrp_diag_weak_s5_long_port(cov=None, pre=None):
    return hierarchical_risk_parity_portfolio_factory(port=weak_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5)


# Diag allocation, but different portfolios

def hrp_unit_diag_s5_port(cov=None, pre=None):
    return hierarchical_risk_parity_portfolio_factory(port=unit_portfolio_factory, alloc=unit_alloc, cov=cov, pre=pre, n_split=5)


def hrp_weak_diag_s5_long_port(cov=None, pre=None):
    return hierarchical_risk_parity_portfolio_factory(port=weak_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5)



HRP_LONG_PORT = [hrp_weak_weak_s5_long_port, hrp_diag_diag_s5_long_port, hrp_diag_weak_s5_long_port, hrp_weak_diag_s5_long_port]
HRP_LS_PORT = [hrp_unit_unit_s5_port, hrp_unit_weak_s5_port, hrp_unit_diag_s5_port]
HRP_PORT = HRP_LONG_PORT + HRP_LS_PORT



if __name__=='__main__':
    from precise.skaters.portfolioutil.portcomparison import m6_equity_portfolio_correlation_rankings
    from pprint import pprint
    rankings = m6_equity_portfolio_correlation_rankings(ports=HRP_PORT, n_dim=40)
    pprint(rankings)