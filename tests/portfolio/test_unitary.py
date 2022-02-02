from precise.skatertools.m6.covarianceforecasting import m6_cov
from precise.skaters.portfolioutil.unitary import weak_from_cov
from precise.skaters.portfolioutil.weak import weak_known_params
from precise.skaters.portfolioutil.ppo import long_from_cov
from precise.skaters.portfolioutil.portfunctions import portfolio_variance, exclude_negative_weights
from pprint import pprint


def dont_test_me_i_take_too_long():
    n_dim = 48
    dfcov0 = m6_cov(interval='d', n_dim=n_dim, n_obs=100)
    cov0 = dfcov0.values
    w0 = weak_from_cov(cov0)
    wl = long_from_cov(cov0)
    v0 = portfolio_variance(cov0, w0)
    vl = portfolio_variance(cov0, wl)
    wn, wn_neg = exclude_negative_weights(w0, with_neg_mass=True)
    vn = portfolio_variance(cov0, wn)

    rankings = [(v0, 'unitary'), (vl, 'long'), (vn, ('exclude',wn_neg))]
    for a in [1.0]:
        for b in [0.8, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2, 1.5]:
            if a >= b:
                wl, neg_mass = weak_known_params(cov=cov0.copy(), a=a, b=b, with_neg_mass=True)
                vl = portfolio_variance(cov=cov0, w=wl)
                rankings.append((vl, (a, b, neg_mass)))
    print(' ')
    pprint(sorted(rankings))


if __name__=='__main__':
    dont_test_me_i_take_too_long()