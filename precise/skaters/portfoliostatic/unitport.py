from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory


def unit_port(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre)


UNIT_PORT = [unit_port]
UNIT_LONG_PORT = []
