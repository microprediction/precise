from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory


def unit_port(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre)


UNIT_LS_PORT = [unit_port]
UNIT_LONG_PORT = []
UNIT_PORT = UNIT_LONG_PORT + UNIT_LS_PORT