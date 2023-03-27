from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory


def unit_port(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre)


def unit_port_p100(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=1.0)


def unit_port_p090(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.9)


def unit_port_p080(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.8)


def unit_port_p070(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.7)


def unit_port_p060(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.6)


def unit_port_p050(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.5)


def unit_port_p040(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.4)


def unit_port_p030(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.3)


def unit_port_p020(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.2)


def unit_port_p010(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.1)


def unit_port_p000(cov=None, pre=None):
    return unit_portfolio_factory(cov=cov, pre=pre, phi=0.0)


UNIT_LS_PORT = [unit_port, unit_port_p000, unit_port_p010, unit_port_p020, unit_port_p030,
                unit_port_p040, unit_port_p050, unit_port_p060, unit_port_p070,
                unit_port_p080, unit_port_p090, unit_port_p100]

UNIT_LONG_PORT = []
UNIT_PORT = UNIT_LONG_PORT + UNIT_LS_PORT