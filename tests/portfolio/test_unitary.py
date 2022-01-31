from precise.skatertools.m6.covarianceforecasting import m6_cov
from precise.skaters.portfolioutil.analytic import unitary_long_from_cov, unitary_from_cov
from precise.skaters.portfolioutil.longonly import long_from_cov
from precise.skaters.portfolioutil.portfunctions import portfolio_variance, exclude_negative_weights
from pprint import pprint


def test_a_few():
    n_dim = 15
    dfcov0 = m6_cov(interval='m',n_dim=n_dim, n_obs=60)
    cov0 = dfcov0.values
    w0 = unitary_from_cov(cov0)
    wl = long_from_cov(cov0)
    v0 = portfolio_variance(cov0,w0)
    vl = portfolio_variance(cov0,wl)
    wn = exclude_negative_weights(w0)
    vn = portfolio_variance(cov0,wn)

    rankings = [(v0,'unitary'),(vl,'long'),(vn,'exclude')]
    for a in [0.5,0.6,0.7,0.8,0.9, 1.0,1.1, 1.2, 1.3, 2.0, 3.0, 8, 15, 23, 235]:
        for b in [0.1,0.2,0.3, 0.4, 0.5,0.6,0.7, 0.8, 0.9,1.0,1.1,1.2, 1.5]:
            try:
                wl, neg_mass = unitary_long_from_cov(cov=cov0.copy(), a=a, b=b, with_neg_mass=True)
                vl = portfolio_variance(cov=cov0, w=wl)
                rankings.append((vl, (a,b,neg_mass)))
            except Exception as e:
                print(e)
                pass
    print(' ')
    pprint(sorted(rankings))




def test_some():
    n_dim = 48
    dfcov0 = m6_cov(interval='d', n_dim=n_dim, n_obs=100)
    cov0 = dfcov0.values
    w0 = unitary_from_cov(cov0)
    wl = long_from_cov(cov0)
    v0 = portfolio_variance(cov0, w0)
    vl = portfolio_variance(cov0, wl)
    wn, wn_neg = exclude_negative_weights(w0, with_neg_mass=True)
    vn = portfolio_variance(cov0, wn)

    rankings = [(v0, 'unitary'), (vl, 'long'), (vn, ('exclude',wn_neg))]
    for a in [1.0]:
        for b in [0.8, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2, 1.5]:
            if a >= b:
                wl, neg_mass = unitary_long_from_cov(cov=cov0.copy(), a=a, b=b, with_neg_mass=True)
                vl = portfolio_variance(cov=cov0, w=wl)
                rankings.append((vl, (a, b, neg_mass)))
    print(' ')
    pprint(sorted(rankings))


if __name__=='__main__':
    test_some()