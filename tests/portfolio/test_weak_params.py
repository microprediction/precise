from precise.skatertools.m6.covarianceforecasting import m6_cov
from precise.skaters.portfoliostatic.unitportfactory import unitary_from_cov
from precise.skaters.portfoliostatic.weakportfactory import _weak_known_params
from precise.skaters.portfolioutil.portfunctions import portfolio_variance, exclude_negative_weights
from pprint import pprint
from precise.skaters.covarianceutil.covrandom import random_band_cov

from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


def test_weak_with_different_params(real_data=False):
    n_dim = 48
    if real_data:
        dfcov0 = m6_cov(interval='d', n_dim=n_dim, n_obs=100)
        cov0 = dfcov0.values
    else:
        cov0 = random_band_cov(n_dim=3, n_bands=3, n=5000)

    w0 = unitary_from_cov(cov=cov0)
    v0 = portfolio_variance(w=w0, cov=cov0)

    wn, wn_neg = exclude_negative_weights(w0, with_neg_mass=True)
    vn = portfolio_variance(w=wn, cov=cov0)

    rankings = [(v0, 'unitary'), (vn, ('exclude', wn_neg))]

    try:
        if using_pyportfolioopt:
            from precise.skaters.portfoliostatic.ppoportfactory import ppo_vol_long_from_cov
            wl = ppo_vol_long_from_cov(cov=cov0)
            vl = portfolio_variance(w=wl, cov=cov0)
            rankings.append((vl, ('optimizer')))
    except:
        print('Optimizer failed')
        pass

    for a in [1.0]:
        for b in [0.8, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2, 1.5]:
            if a >= b:
                wl, neg_mass = _weak_known_params(cov=cov0.copy(), a=a, b=b, w0=w0, with_neg_mass=True)
                vl = portfolio_variance(cov=cov0, w=wl)
                rankings.append((vl, (a, b, neg_mass)))
    print(' ')
    pprint(sorted(rankings, key=lambda x: x[0]))


if __name__ == '__main__':
    test_weak_with_different_params(real_data=False)
