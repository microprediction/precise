from precise.skatertools.m6.covarianceforecasting import m6_cov
from precise.skaters.portfoliostatic.weakportfactory import _weak_from_cov, _weak_optimal_b
from precise.skaters.portfolioutil.portfunctions import portfolio_variance, exclude_negative_weights
from pprint import pprint
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def dont_test_me_i_take_too_long():
    if using_pyportfolioopt:
        from precise.skaters.portfoliostatic.ppoportfactory import ppo_vol_long_from_cov
        n_dim = 95
        dfcov0 = m6_cov(interval='d', n_dim=n_dim, n_obs=140)
        cov0 = dfcov0.values
        w0 = _weak_from_cov(cov0)
        wl = ppo_vol_long_from_cov(cov0)
        v0 = portfolio_variance(cov0, w0)
        vl = portfolio_variance(cov0, wl)
        wn, wn_neg = exclude_negative_weights(w0, with_neg_mass=True)
        vn = portfolio_variance(cov0, wn)
        wm, wm_neg = _weak_optimal_b(cov=cov0, with_neg_mass=True)
        vm = portfolio_variance(cov0.copy(), wm)

        rankings = [(v0, 'unitary'), (vl, 'long'), (vn, ('exclude', wn_neg)), (vm,('minimize',wm_neg))]
        print(' ')
        pprint(sorted(rankings))


if __name__=='__main__':
    dont_test_me_i_take_too_long()