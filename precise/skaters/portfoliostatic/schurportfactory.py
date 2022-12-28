from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.diagalloc import diag_alloc
from pprint import pprint
from precise.skaters.portfoliostatic.schurportutil import schur_augmentation, symmetric_step_up_matrix, even_split
import numpy as np
from precise.skaters.portfoliostatic.equalport import equal_long_port
from precise.skaters.covarianceutil.covrandom import jiggle_cov
from precise.skaters.covarianceutil.covfunctions import cov_distance, try_invert


def schur_portfolio_factory(cov=None, pre=None, port=None, port_kwargs=None,
                            alloc=None, alloc_kwargs=None,
                            n_split=5, gamma=1.0, delta=0.0,
                            seriation_depth=10, jiggle=True):
    """
         A divide and conquer allocation strategy using seriation, and augmented sub-covariancecomparisonutil matrices

    :param cov:
    :param port:                Method to use on leaves
    :param port_kwargs:
    :param alloc:               Method to use to allocate
    :param alloc_kwargs:
    :param n_split:             Minimum size to split
    :param gamma:
    :param delta:
    :param seriation_depth:
    :return:
    """

    if cov is None:
        cov = try_invert(pre)

    splitter = even_split
    splitter_kwargs = {'n_split':n_split}
    from precise.skaters.covarianceutil.covfunctions import seriation
    seriator = seriation
    seriator_kwargs = {}

    if jiggle:
        jiggled_cov = jiggle_cov(cov=cov)
    else:
        jiggled_cov = np.copy(cov)

    return hierarchical_schur_complementary_portfolio_with_defaults(seriator=seriator, seriator_kwargs=seriator_kwargs,
                                                                    seriation_depth=seriation_depth,
                                                                    port=port, port_kwargs=port_kwargs,
                                                                    alloc=alloc, alloc_kwargs=alloc_kwargs,
                                                                    splitter=splitter, splitter_kwargs=splitter_kwargs,
                                                                    cov=jiggled_cov,
                                                                    gamma=gamma, delta=delta)


def hierarchical_schur_complementary_portfolio_with_defaults(cov=None, port=None, port_kwargs=None,
                                                             alloc=None, alloc_kwargs=None,
                                                             splitter=None, splitter_kwargs=None,
                                                             seriator=None, seriator_kwargs=None,
                                                             seriation_depth=10,
                                                             delta=0.0, gamma=1.0):

    if alloc is None:
        alloc = diag_alloc

    if port is None:
        port = diagonal_portfolio_factory

    if port_kwargs is None:
        port_kwargs = {}

    if alloc_kwargs is None:
        alloc_kwargs = {}

    return hierarchical_schur_complementary_portfolio(cov=cov, port=port, port_kwargs=port_kwargs,
                                                      alloc=alloc, alloc_kwargs=alloc_kwargs,
                                                      splitter=splitter, splitter_kwargs=splitter_kwargs,
                                                      seriator = seriator, seriator_kwargs=seriator_kwargs,
                                                      seriation_depth=seriation_depth,
                                                      delta=delta, gamma=gamma)


def hierarchical_schur_complementary_portfolio(cov, port, port_kwargs,
                                               alloc, alloc_kwargs,
                                               splitter, splitter_kwargs,
                                               seriator, seriator_kwargs,
                                               seriation_depth,
                                               delta, gamma):
    """
        An experimental way to split allocation
    """
    n = np.shape(cov)[0]
    n1, n2 = splitter(cov, **splitter_kwargs)
    assert n1+n2==n
    if n1<=1 or n2<=1:
        # If the portfolio is not too big, apply to leaves directly
        w = port(cov, **port_kwargs)
        if isinstance(w,list):
            print('Warning: '+port.__name__+' returns list not array ')
            w = np.array(w)
        return w
    else:
        # 1. Establish ordering, or bail out altogether
        if any(np.diag(cov) < 1e-8):
            return equal_long_port(cov=cov)
        elif seriation_depth<=0:
            ndx = list(range(n1+n2))
        else:
            cov_dist = cov_distance(cov)
            ndx = seriator(cov_dist, **seriator_kwargs)
        inv_ndx = np.argsort(ndx)
        cov_cols = cov[:, ndx]
        cov_back = cov_cols[:, inv_ndx]
        assert np.allclose(cov, cov_back)
        ordered_cov = cov_cols[ndx, :]

        # 2. Split
        A = ordered_cov[:n1, :n1]
        D = ordered_cov[n1:, n1:]
        B = ordered_cov[:n1, n1:]
        C = ordered_cov[n1:, :n1]  #  = B.T

        # 3. Augment and allocate
        Ag, Dg, info = schur_augmentation(A=A, B=B, C=C, D=D, gamma=gamma)
        aA, aD = alloc(covs=[Ag, Dg])
        if True:
            # 3a. Just for interest, compare allocations. This is research code :)
            aA_original, aD_original = alloc(covs=[A, D])
            allocationRatioA = (aA / aA_original)
            info.update({'allocationRatioA':allocationRatioA})
            if False:
                pprint({'allocationRatioA':allocationRatioA})

        # Sub-allocate
        wA = hierarchical_schur_complementary_portfolio(cov=Ag, port=port, port_kwargs=port_kwargs,
                                                       alloc=alloc, alloc_kwargs=alloc_kwargs,
                                                       splitter=splitter, splitter_kwargs=splitter_kwargs,
                                                       seriator=seriator, seriator_kwargs=seriator_kwargs,
                                                       seriation_depth = seriation_depth-1,
                                                       delta=delta, gamma=gamma)
        wD = hierarchical_schur_complementary_portfolio(cov=Dg, port=port, port_kwargs=port_kwargs,
                                                        alloc=alloc, alloc_kwargs=alloc_kwargs,
                                                        splitter=splitter, splitter_kwargs=splitter_kwargs,
                                                        seriator=seriator, seriator_kwargs=seriator_kwargs,
                                                        seriation_depth=seriation_depth - 1,
                                                        delta=delta, gamma=gamma)
        # Reconstruct
        ordered_w = np.concatenate([aA * np.array(wA), aD * np.array(wD)])

        # Undo seriation ordering
        try:
            w = ordered_w[inv_ndx]
        except TypeError:
            print('Warning: ' + port.__name__ + ' returns list not array - should really fix this ')
            w = np.array(ordered_w)[inv_ndx]
        return np.array(w)



if __name__=='__main__':
    M = symmetric_step_up_matrix(n1=7, n2=6)
    print(np.dot(M, np.ones(6)))
    print(np.dot(M.transpose()*6/7,np.ones(7)))
