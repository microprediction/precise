from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
import numpy as np
from functools import partial
from precise.skaters.portfolioutil.seriation import corr_seriation_portfolio_factory
from precise.skaters.covarianceutil.covfunctions import top_schur_complement, multiply_by_inverse, \
    bottom_schur_complement, to_symmetric, inverse_multiply
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from pprint import pprint

# Acca Dacca Portfolio method
#
# It's gonna rock you
#
# But a work in progress


def prc_acdc_weak_5(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=weak_portfolio_factory, cov=cov, pre=pre, n_split=5)


def prc_acdc_weak_25(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=weak_portfolio_factory, cov=cov, pre=pre, n_split=25)


def prc_acdc_diag_5(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=diagonal_portfolio_factory, cov=cov, pre=pre, n_split=5)


def prc_acdc_diag_25(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=diagonal_portfolio_factory, cov=cov, pre=pre, n_split=25)


def prc_acdc_unit_5(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=unit_portfolio_factory, cov=cov, pre=pre, n_split=5)


def prc_acdc_unit_25(cov=None, pre=None):
    return schur_complement_portfolio_factory(port=unit_portfolio_factory, cov=cov, pre=pre, n_split=25)



HRP_PORT = [ prc_acdc_weak_5, prc_acdc_weak_25, prc_acdc_weak_5, prc_acdc_weak_25 ]


def even_split(cov, n_split=5)->(float,float):
    """
        This simple method is the default, for now, but I'm working on a better one
    """
    try:
        n_dim = np.shape(cov)[0]
    except IndexError:
        print('huh')
        raise ValueError('not good')
    if n_dim<=n_split:
        return (n_dim,0)
    else:
        n1 = int(n_dim / 2)
        n2 = n_dim - n1
        return n1, n2


def schur_complement_portfolio_factory(seriator=None, port=None, splitter=None, cov=None, pre=None, n_split=5, c:[float]=None):
    """
        This is not a standard technique, as far as I know.
        It is my attempt to unify two quite different approaches (top down versus optimization)
        As compared with hierarchical risk parity (say) this uses conditional covariances (schur complement)
        It is motivated by the unitary case:

    :param port:       The portfolio generator eventually used on small portfolios    port( cov ) -> [ float ]
    :param splitter:   A function taking cov matrix and returning (n1,n2), telling us how to bisect the problem
    :param c:          The coefficients in the constraint   w^T c = 1
                       (This "c" vector defaults to a vector of ones)
    :return:
    """

    if port is None:
        port = diagonal_portfolio_factory

    if splitter is None:
        splitter = partial( even_split, n_split=n_split )


    port_kwargs = {'splitter':splitter,'port':port,'c':c}
    return corr_seriation_portfolio_factory(seriator=seriator, port=_acca_dacca_portfolio, port_kwargs=port_kwargs, cov=cov, pre=pre)


def _acca_dacca_portfolio(cov, port, splitter):
    """
        Assumes assets have been ordered to try to reduce the importance of "B"
        (How best to do that remains an open question)

    """
    n1, n2 = splitter(cov=cov)
    assert n1+n2 == np.shape(cov)[0]
    if n1==0 or n2==0:
        return port(cov)
    else:
        #           C   = [ [ A, B ]
        #                   [ B, D ] ]
        n = n1+n2
        A = cov[:n1,:n1]
        B = cov[:n1,n1:]
        C = cov[n1:,:n1]
        D = cov[n1:,n1:]
        Ac = to_symmetric( top_schur_complement(A=A, B=B, C=C, D=D ) )
        Dc = to_symmetric( bottom_schur_complement(A=A, B=B, C=C, D=D) )

        B_Dinv = multiply_by_inverse(B,D)  # B D^{-1}
        C_Ainv = multiply_by_inverse(C,A)  # B A^{-1}
        R = np.block([
                        [ np.eye(n1),        -B_Dinv ],
                        [ -C_Ainv    ,        np.eye(n2) ]
                    ])


        VERIFY_MATRIX_IDENTITY = True
        if VERIFY_MATRIX_IDENTITY:
            # debuggin'
            C_tilde = np.block( [
                          [ Ac,  np.zeros(shape=(n1,n2)) ],
                          [ np.zeros(shape=(n2,n1)), Dc  ]
            ])
            C_inv = inverse_multiply(C_tilde,R)
            pre = np.linalg.inv(cov)
            assert np.allclose( C_inv, pre )

        c = np.ones(n)
        c_tilde = np.dot(R, c)
        cA_tilde = c_tilde[:n1]
        cD_tilde = c_tilde[n1:]

        A_tilde = Ac
        D_tilde = Dc

        # Solve transformed problem
        wA_tilde = _acca_dacca_portfolio(cov=Ac, port=port, splitter=splitter)
        wD_tilde = _acca_dacca_portfolio(cov=Dc, port=port, splitter=splitter)

        # Allocate based on unitary portfolios
        from precise.skaters.portfoliostatic.unitportfactory import rescaled_unit_from_cov
        uA = rescaled_unit_from_cov(cov=Ac, c=cA_tilde)
        uD = rescaled_unit_from_cov(cov=Dc, c=cD_tilde)

        # this is all wrong, need to fix it

        massA = np.sum( np.linalg.solve(Ac,cA_tilde) )
        massB = np.sum( np.linalg.solve(Dc,cD_tilde) )

        varA = portfolio_variance(cov=Ac, w=wA_tilde)
        varD = portfolio_variance(cov=Dc, w=wD_tilde)
        cA_tilde = cA_tilde/varA
        cD_tilde = cD_tilde /varD
        c_tilde = np.concatenate([cA_tilde, cD_tilde])
        w_raw = np.linalg.solve(R, c_tilde)       # <-- But now diagonal terms come into play again
        assert np.allclose( np.dot(R,w_raw), c_tilde )
        from precise.skaters.locationutil.vectorfunctions import normalize
        w = normalize(w_raw)

        CURIOUS = False
        if CURIOUS:
            # Just for interest, check the impact of diagonal terms
            massA = np.sum(w[:n1])/np.sum(w)
            diagMassA = (1/varA)/(1/varA+1/varD)
            from precise.skaters.portfoliostatic.diagportfactory import prc_diag_alloc
            invMassA, invMassD = prc_diag_alloc([A,D])
            invMassA_tilde, invMassB_tilde = prc_diag_alloc([Ac, Dc])

            aAllocations = {'inv':invMassA,'inv_cond':invMassA_tilde,
                            'diag':diagMassA,'schur':massA}
            from pprint import pprint
            pprint(aAllocations)
            pass

        return w


if __name__=='__main__':
    from precise.skatertools.syntheticdata.factor import create_disjoint_factor_dataset, create_factor_dataset
    x = create_disjoint_factor_dataset(n_dims=[5,5], n=100)
    x = create_factor_dataset(n=200,n_dim=8)
    cov = np.cov(x, rowvar=False)
    from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
    corr = cov_to_corrcoef(cov)

    # Compare in-sample portfolio variance
    from precise.skaters.portfoliostatic.hrpportfactory import prc_hrp_diag_n5_g0, prc_hrp_weak_n5_g0, prc_hrp_unit_n5_g0
    from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory

    uv = portfolio_variance(cov=cov, w=unit_portfolio_factory(cov=cov))
    report = {'unitary': portfolio_variance(cov=cov, w=unit_portfolio_factory(cov=cov)) / uv,
              'divide and condition (unit)':portfolio_variance(cov=cov,w=prc_acdc_unit_5(cov=cov))/uv,
              'divide and condition (diag)': portfolio_variance(cov=cov, w=prc_acdc_diag_5(cov=cov))/uv,
              'divide and condition (weak)': portfolio_variance(cov=cov, w=prc_acdc_weak_5(cov=cov))/uv,
              'hierarchical risk parity (diag)': portfolio_variance(cov=cov, w=prc_hrp_diag_n5_g0(cov=cov)) / uv,
              'hierarchical risk parity (weak)': portfolio_variance(cov=cov, w=prc_hrp_weak_n5_g0(cov=cov)) / uv,
              'hierarchical risk parity (unit)': portfolio_variance(cov=cov, w=prc_hrp_unit_n5_g0(cov=cov)) / uv,
              }
    print(' ')
    pprint(report)
