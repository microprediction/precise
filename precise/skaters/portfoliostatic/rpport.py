from precise.skaters.portfoliostatic.rpportfactory import rp_portfolio_factory
from precise.skaters.covarianceutil.covfunctions import multiply_diag


def rp_port_p100(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre, phi=1.0)


def rp_port_p90(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.9)


def rp_port_p80(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov,pre=pre,phi=0.8)


def rp_port_p70(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.7)


def rp_port_p60(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.6)


def rp_port_p50(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.5)


def rp_port_p40(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.4)


def rp_port_p30(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.3)


def rp_port_p20(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.2)


def rp_port_p10(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.1)


def rp_port_p0(cov=None, pre=None):
    return rp_portfolio_factory(cov=cov, pre=pre,phi=0.0)


RP_LONG_PORT = [rp_port_p100, rp_port_p70, rp_port_p80, rp_port_p90,
                rp_port_p40, rp_port_p50, rp_port_p60,
                rp_port_p10, rp_port_p20, rp_port_p30, rp_port_p0]