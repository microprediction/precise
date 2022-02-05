from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory


def diag_long_port(cov=None, pre=None):
    return diagonal_portfolio_factory(cov=cov, pre=pre)


DIAG_LONG_PORT = [ diag_long_port ]
DIAG_PORT = DIAG_LONG_PORT