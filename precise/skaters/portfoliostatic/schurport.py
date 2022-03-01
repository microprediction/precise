from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
from precise.skaters.portfoliostatic.schurportfactory import schur_portfolio_factory
from precise.skaters.portfoliostatic.diagalloc import diag_alloc
from precise.skaters.portfoliostatic.unitalloc import unit_alloc
from precise.skaters.portfoliostatic.weakalloc import weak_long_alloc

# Schur complement portfolios 

# Some that use the same portfolio constructor as allocation...


def schur_unit_unit_s5_g100_port(cov=None, pre=None):
    return schur_portfolio_factory(port=unit_portfolio_factory, alloc=unit_alloc, cov=cov, pre=pre, n_split=5, gamma=1.0)


def schur_weak_weak_s5_g100_long_port(cov=None, pre=None):
    return schur_portfolio_factory(port=weak_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5, gamma=1.0)


def schur_diag_diag_s5_g100_long_port(cov=None, pre=None):
    return schur_portfolio_factory(port=diagonal_portfolio_factory, alloc=diag_alloc, cov=cov, pre=pre, n_split=5, gamma=1.0)


def schur_unit_unit_s5_g050_port(cov=None, pre=None):
    return schur_portfolio_factory(port=unit_portfolio_factory, alloc=unit_alloc, cov=cov, pre=pre, n_split=5, gamma=0.5)


def schur_weak_weak_s5_g050_long_port(cov=None, pre=None):
    return schur_portfolio_factory(port=weak_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5, gamma=0.5)


def schur_diag_diag_s5_g050_long_port(cov=None, pre=None):
    return schur_portfolio_factory(port=diagonal_portfolio_factory, alloc=diag_alloc, cov=cov, pre=pre, n_split=5, gamma=0.5)




def schur_unit_weak_s5_g100_port(cov=None, pre=None):
    return schur_portfolio_factory(port=unit_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5, gamma=1.0)


def schur_diag_weak_s5_g100_long_port(cov=None, pre=None):
    return schur_portfolio_factory(port=diagonal_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5, gamma=1.0)


def schur_unit_weak_s5_g050_port(cov=None, pre=None):
    return schur_portfolio_factory(port=unit_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5, gamma=0.5)


def schur_diag_weak_s5_g050_long_port(cov=None, pre=None):
    return schur_portfolio_factory(port=diagonal_portfolio_factory, alloc=weak_long_alloc, cov=cov, pre=pre, n_split=5, gamma=0.5)



SCHUR_LONG_PORT = [schur_diag_diag_s5_g100_long_port, schur_weak_weak_s5_g100_long_port,
                   schur_diag_diag_s5_g050_long_port, schur_weak_weak_s5_g050_long_port]
SCHUR_LS_PORT = [schur_unit_unit_s5_g100_port, schur_unit_unit_s5_g050_port]
SCHUR_PORT = SCHUR_LONG_PORT + SCHUR_LS_PORT



if __name__=='__main__':
    from precise.skaters.portfolioutil.portcomparison import m6_equity_portfolio_variance_rankings
    from precise.skaters.portfoliostatic.hrpport import HRP_PORT
    from pprint import pprint
    rankings = m6_equity_portfolio_variance_rankings(ports=SCHUR_PORT + HRP_PORT, n_dim=50)
    pprint(rankings)