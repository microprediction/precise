from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.diagalloc import diag_alloc
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
import numpy as np
from pprint import pprint
from functools import partial
from precise.skaters.portfolioutil.seriation import corr_seriation_portfolio_factory
from precise.skaters.covarianceutil.covfunctions import top_schur_complement, bottom_schur_complement, to_symmetric


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


def risk_parity_portfolio_factory(seriator=None, alloc=None, port=None, splitter=None, cov=None, pre=None, n_split=5, gamma=0.0):
    """
        A class of algorithms that hierarchically allocate capital
        By default this implements Lopez de Prado's 2016 paper (I think)

    :param alloc:      Decides how much capital to split between portfolios  [covs] -> [ float ]
    :param port:       Computes a portfolio     cov -> [ float ]    (Used on the leaves only)
    :param splitter:   Splits into two groups   cov -> (n1,n2)
    :param gamma:      (0,1) How far to move towards Schur complement
    :return:
    """
    # Remark. The port and alloc need not be cut from the same cloth

    if alloc is None:
        alloc = diag_alloc

    if port is None:
        port = diagonal_portfolio_factory

    if splitter is None:
        splitter = partial( even_split, n_split=n_split )

    port_kwargs = {'alloc':alloc,'splitter':splitter,'port':port,'gamma':gamma}
    return corr_seriation_portfolio_factory(seriator=seriator, port=_risk_parity_portfolio, port_kwargs=port_kwargs, cov=cov, pre=pre)


def _risk_parity_portfolio(alloc, cov, port, splitter, gamma:float=0.0):
    """
        Assumes assets have been ordered
    """
    # https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678
    n1, n2 = splitter(cov)
    if n1==0 or n2==0:
        w = port(cov)
        if isinstance(w,list):
            print('Warning: '+port.__name__+' returns list not array ')
            w = np.array(w)
        return w
    else:
        A = cov[:n1,:n1]
        D = cov[n1:,n1:]

        if abs(gamma)>0.0:
            B = cov[:n1, n1:]
            C = cov[n1:, :n1]
            Ac = to_symmetric(top_schur_complement(A=A, B=B, C=C, D=D, gamma=gamma))
            Dc = to_symmetric(bottom_schur_complement(A=A, B=B, C=C, D=D, gamma=gamma))
        else:
            Ac = A
            Dc = D

        wA = _risk_parity_portfolio(alloc=alloc, cov=Ac, port=port, splitter=splitter)
        wD = _risk_parity_portfolio(alloc=alloc, cov=Dc, port=port, splitter=splitter)
        aA, aD = alloc(covs=[Ac,Dc])
        try:
            w = np.concatenate( [aA*np.array(wA), aD*np.array(wD)] )
        except TypeError:
            print('WTF')
            raise ValueError
        return np.array(w)


