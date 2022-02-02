from precise.skaters.portfolioutil.diagonal import prc_diag_alloc, prc_diag_port
from precise.skaters.portfolioutil.weak import prc_weak_port
import numpy as np
from functools import partial
from precise.skaters.portfolioutil.seriation import corr_seriation_portfolio_factory


def prc_ep_weak_5(cov=None, pre=None):
    return enhanced_precision_portfolio_factory(port=prc_weak_port, cov=cov, pre=pre, n_split=5)


def prc_ep_weak_25(cov=None, pre=None):
    return enhanced_precision_portfolio_factory(port=prc_weak_port, cov=cov, pre=pre, n_split=25)


def prc_ep_diag_5(cov=None, pre=None):
    return enhanced_precision_portfolio_factory(port=prc_diag_port, cov=cov, pre=pre, n_split=5)


def prc_ep_diag_25(cov=None, pre=None):
    return enhanced_precision_portfolio_factory(port=prc_diag_port, cov=cov, pre=pre, n_split=25)


HRP_PORT = [ prc_ep_weak_5, prc_ep_weak_25, prc_ep_weak_5, prc_ep_weak_25 ]


def even_split(cov, n_split=5)->(float,float):
    """
        Parity methods require some way of splitting assets into two groups
        This simple method is the default
    """
    n_dim = np.shape(cov)[0]
    if n_dim<=n_split:
        return (n_dim,0)
    else:
        n1 = int(n_dim / 2)
        n2 = n_dim - n1
        return n1, n2


def enhanced_precision_portfolio_factory(seriator=None, alloc=None, port=None, splitter=None, cov=None, pre=None, n_split=5):
    """
        A class of algorithms that hierarchically allocate capital

        However, unlike HRP these take block diagonal terms into account

    :param alloc:      Decides how much capital to split between portfolios  [covs] -> [ float ]
    :param port:       Computes a portfolio     cov -> [ float ]    (Used on the leaves only)
    :param splitter:   Splits into two groups   cov -> (n1,n2)
    :return:
    """
    # Remark. The port and alloc need not be cut from the same cloth

    if alloc is None:
        alloc = prc_diag_alloc

    if port is None:
        port = prc_diag_port

    if splitter is None:
        splitter = partial( even_split, n_split=n_split )

    port_kwargs = {'alloc':alloc,'splitter':splitter,'port':port}
    return corr_seriation_portfolio_factory(seriator=seriator, port=_enhanced_precision_portfolio, port_kwargs=port_kwargs, cov=cov, pre=pre)


def _enhanced_precision_portfolio(alloc, cov, port, splitter):
    """
        Assumes assets have been ordered
    """
    # https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678
    n1, n2 = splitter(cov)
    if n1==0 or n2==0:
        return port(cov)
    else:
        A = cov[:n1,:n1]
        D = cov[n1:,n1:]
        wA = _enhanced_precision_portfolio(alloc=alloc, cov=A, port=port, splitter=splitter)
        wD = _enhanced_precision_portfolio(alloc=alloc, cov=D, port=port, splitter=splitter)
        aA, aD = alloc(covs=[A,D])
        w = np.concatenate( [aA*wA, aD*wD] )
        return w


if __name__=='__main__':
    from precise.skaters.covarianceutil.covrandom import random_band_cov
    cov = random_band_cov()
    print(np.shape(cov))
    w = prc_ep_diag_5(cov=cov)
    print(sum(w))