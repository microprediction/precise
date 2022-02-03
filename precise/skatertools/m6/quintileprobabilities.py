import numpy as np
import pandas as pd
from precise.skatertools.m6.covarianceforecasting import m6_cov
from precise.skatertools.m6.tilting import affection_tilt

# M6 Quintile probability estimates by Monte Carlo


def what_pctl_number_of(x, a, pctls=[20,40,60,80]):
    return np.argmax(np.sign(np.append(np.percentile(x, pctls), np.inf) - a))


def mvn_quintile_probabilities(sgma, n_samples, mu=None):
    n_dim = np.shape(sgma)[0]
    if mu is None:
        mu = np.zeros(n_dim)
    x =  np.random.multivariate_normal(mu, sgma, size=n_samples, check_valid='warn', tol=1e-8)
    y = scores_to_quintiles(x)
    p = list()
    for i in range(5):
        pi = np.mean(y==i,axis=0)
        p.append(pi)
    return p


def scores_to_quintiles(x):
    ys = list()
    for xi in x:
        q = np.quantile(x,[0.2,0.4,0.6,0.8])
        y = np.searchsorted(q, xi)
        ys.append(y)
    return np.array(ys)



def m6_probabilities(f, interval='d',n_dim=100, n_samples=5000, n_obs=200, verbose=False, love=None, hate=None, intensity=1.0):
    if verbose:
        print('   ... retrieving data and estimating covariance')
    covdf = m6_cov(f=f, interval=interval, n_dim=n_dim, n_obs=n_obs)
    tickers = list(covdf.columns)
    sgma = covdf.values
    mu = affection_tilt(covdf=covdf, love=love, hate=hate, intensity=intensity)

    if verbose:
        print('   ... performing Monte Carlo for rank probabilities')

    p = mvn_quintile_probabilities(mu=mu, sgma=sgma, n_samples=n_samples)
    df = pd.DataFrame(columns=tickers, data=p).transpose()
    df_cov = pd.DataFrame(columns=tickers, index=tickers, data=sgma)
    return df, df_cov


if __name__=='__main__':
    df = m6_probabilities(n_dim=5)




