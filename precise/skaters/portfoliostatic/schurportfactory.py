from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.diagalloc import diag_alloc
import numpy as np
from pprint import pprint
from functools import partial
from precise.skaters.portfolioutil.seriation import corr_seriation_portfolio_factory
from precise.skaters.covarianceutil.covfunctions import schur_complement, \
    to_symmetric, multiply_by_inverse, inverse_multiply, is_positive_def, nearest_pos_def
from scipy.optimize import root_scalar
from precise.skaters.portfoliostatic.schurportutil import symmetric_step_up_matrix, even_split



def hierarchical_seriation_portfolio_factory(seriator=None, alloc=None, port=None, splitter=None, cov=None, pre=None, n_split=5, gamma=0.0, delta=0.0):
    """
        A class of algorithms that

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

    port_kwargs = {'alloc':alloc,'splitter':splitter,'port':port,'gamma':gamma, 'delta':delta}
    return corr_seriation_portfolio_factory(seriator=seriator, port=hierarchical_seriated_portfolio_factory, port_kwargs=port_kwargs, cov=cov, pre=pre)


def hierarchical_seriated_portfolio_factory(alloc, cov, port, splitter, gamma:float=0.0, delta:float=0):
    """
        Assumes assets have been ordered already
    """
    n1, n2 = splitter(cov)
    if n1==0 or n2==0:
        w = port(cov)
        if isinstance(w,list):
            print('Warning: '+port.__name__+' returns list not array ')
            w = np.array(w)
        return w
    else:
        if abs(gamma)<1e-6:
            # Hierarchical risk parity (Lopez de Prado)
            w = hierarchical_risk_parity(cov=cov, n1=n1, port=port, alloc=alloc, splitter=splitter)
        else:
            # Schur complementary portfolio construction (yours truly)
            w = hierarchical_schur_complementary_portfolio(cov=cov, n1=n1, port=port, alloc=alloc, splitter=splitter, gamma=gamma, delta=delta)
        return w


def hierarchical_risk_parity(cov, n1, port, alloc, splitter):
    """
         Recursive hierarchical risk parity
    """
    # https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678
    A = cov[:n1, :n1]
    D = cov[n1:, n1:]
    wA = hierarchical_seriated_portfolio_factory(alloc=alloc, cov=A, port=port, splitter=splitter, gamma=0.0)
    wD = hierarchical_seriated_portfolio_factory(alloc=alloc, cov=D, port=port, splitter=splitter, gamma=0.0)
    aA, aD = alloc(covs=[A, D])
    w = np.concatenate([aA * np.array(wA), aD * np.array(wD)])
    return w


def pseudo_schur_complement(A, B, C, D, gamma):
    """
       Augmented cov matrix for "A" inspired by the Schur complement
    """
    Ac_raw = schur_complement(A=A, B=B, C=C, D=D, gamma=gamma)
    nA = np.shape(A)[0]
    nD = np.shape(D)[0]
    Ac = to_symmetric(Ac_raw)
    M = symmetric_step_up_matrix(n1=nA, n2=nD)
    Mt = np.transpose(M)
    BDinv = multiply_by_inverse(B, D)
    BDinvMt = np.dot(BDinv, Mt)
    Ra = np.eye(nA) - gamma * BDinvMt
    Ag = inverse_multiply(Ra, Ac)
    return Ag


def _maximal_gamma(A,B,C,D):

    def _gamma_objective(gamma, A, B, C, D):
        Ag = pseudo_schur_complement(A=A, B=B, C=C, D=D, gamma=gamma)
        Dg = pseudo_schur_complement(A=D, B=C, C=B, D=A, gamma=gamma)
        pos_def = is_positive_def(Ag) and is_positive_def(Dg)
        return -0.01 if pos_def else 1.0

    try:
        sol = root_scalar(f=_gamma_objective, args=(A,B,C,D), method='bisect', x0=0.25,
                          x1=0.5, xtol=0.01, bracket=(0,0.95), maxiter=10)
        return min(max(sol.root - 0.1, 0), 1.0)
    except ValueError:
        return 0.0


def hierarchical_schur_complementary_portfolio(cov, n1, port, alloc, splitter, delta=0.0, gamma=0.5):
    """
        An experimental way to split allocation
    """
    A = cov[:n1, :n1]
    D = cov[n1:, n1:]
    B = cov[:n1, n1:]
    C = cov[n1:, :n1]  #  = B.T

    if delta>0:
        # Haven't tried this yet :)
        rhoB = np.mean(B,axis=None)
        rhoCov_raw = cov - rhoB*np.ones_like(cov)
        rhoCov = nearest_pos_def(rhoCov_raw)
        return hierarchical_schur_complementary_portfolio(cov=rhoCov, n1=n1, port=port, alloc=alloc, splitter=splitter, gamma=gamma)
    else:
        if gamma>0.0:
            # Augment the cov matrices before passing down
            max_gamma = _maximal_gamma(A=A, B=B, C=C, D=D)
            augA = pseudo_schur_complement(A=A, B=B, C=C, D=D, gamma=gamma * max_gamma)
            augD = pseudo_schur_complement(A=D, B=C, C=B, D=A, gamma=gamma * max_gamma)
            if not is_positive_def(augA):
                Ag = nearest_pos_def(augA)
            else:
                Ag = augA
            if not is_positive_def(augD):
                Dg = nearest_pos_def(augD)
            else:
                Dg = augD
            reductionD = np.linalg.norm(Dg)/np.linalg.norm(D)
            reductionA = np.linalg.norm(Ag)/np.linalg.norm(A)
            reductionRatioA = reductionA/reductionD
        else:
            reductionRatioA = 1.0
            Ag = A
            Dg = D
        wA = hierarchical_seriated_portfolio_factory(alloc=alloc, cov=Ag, port=port, splitter=splitter, gamma=gamma)
        wD = hierarchical_seriated_portfolio_factory(alloc=alloc, cov=Dg, port=port, splitter=splitter, gamma=gamma)
        aA, aD = alloc(covs=[Ag, Dg])
        aA_original, aD_original = alloc( covs=[A,D])
        allocationRatioA = (aA/aA_original)
        info = {'reductionA':reductionA,
                'reductionD':reductionD,
                'reductionRatioA':reductionRatioA,
                'allocationRatioA':allocationRatioA}
        pprint(info)
        w = np.concatenate([aA * np.array(wA), aD * np.array(wD)])
        return np.array(w)


if __name__=='__main__':
    M = symmetric_step_up_matrix(n1=7, n2=6)
    print(np.dot(M, np.ones(6)))
    print(np.dot(M.transpose()*6/7,np.ones(7)))