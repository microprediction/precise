from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.acdcfactory import schur_complement_portfolio_factory

# Acca Dacca Portfolio method
#
# It's gonna rock you ... eventually


def acdc_weak_s5_port(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=weak_portfolio_factory, cov=cov, pre=pre, n_split=5)


def acdc_weak_s25_port(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=weak_portfolio_factory, cov=cov, pre=pre, n_split=25)


ACDC_PORT = []   # Not working yet
ACDC_LONG_PORT = []
