import numpy as np
import pandas as pd
from pprint import pprint
from precise.skatertools.m6.covarianceforecasting import m6_cov

def what_pctl_number_of(x, a, pctls=[20,40,60,80]):
    return np.argmax(np.sign(np.append(np.percentile(x, pctls), np.inf) - a))

def mvn_quintile_probabilities(sgma, n_samples):
    from winning.lattice_simulation import placegetters_from_performances
    n_dim = np.shape(sgma)[0]
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


def m6_probabilities(interval='d',n_dim=100, n_samples=5000, n_obs=200):
    covdf = m6_cov(interval=interval, n_dim=n_dim, n_obs=n_obs)
    tickers = list(covdf.columns)
    sgma = covdf.values
    p = mvn_quintile_probabilities(sgma=sgma, n_samples=n_samples)
    df = pd.DataFrame(columns=tickers, data=p).transpose()
    return df


if __name__=='__main__':
    df = m6_probabilities(interval='d',n_dim=100, n_obs=300, n_samples=5000)
    print(df[:7])
    df.to_csv('probabilities.csv')




