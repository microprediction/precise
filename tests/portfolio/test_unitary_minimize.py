from precise.skatertools.m6.covarianceforecasting import m6_cov
from precise.skaters.portfolioutil.analytic import unitary_long_from_cov, unitary_from_cov, unitary_long_gradual, unitary_long_mininize
from precise.skaters.portfolioutil.longonly import long_from_cov
from precise.skaters.portfolioutil.portfunctions import portfolio_variance, exclude_negative_weights
from pprint import pprint


def dont_test_me():
    n_dim = 95
    dfcov0 = m6_cov(interval='d', n_dim=n_dim, n_obs=140)
    cov0 = dfcov0.values
    w0 = unitary_from_cov(cov0)
    wl = long_from_cov(cov0)
    v0 = portfolio_variance(cov0, w0)
    vl = portfolio_variance(cov0, wl)
    wn, wn_neg = exclude_negative_weights(w0, with_neg_mass=True)
    vn = portfolio_variance(cov0, wn)
    wg, wg_neg = unitary_long_gradual(cov0, with_neg_mass=True)
    vg = portfolio_variance(cov0.copy(), wg)
    wm, wm_neg = unitary_long_mininize(cov0, with_neg_mass=True)
    vm = portfolio_variance(cov0.copy(), wm)

    rankings = [(v0, 'unitary'), (vl, 'long'), (vn, ('exclude', wn_neg)), (vg,('gradual',wg_neg)), (vm,('minimize',wm_neg))]
    print(' ')
    pprint(sorted(rankings))


if __name__=='__main__':
    dont_test_me()