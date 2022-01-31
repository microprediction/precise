import numpy as np
import pandas as pd
from pprint import pprint
from precise.skatertools.m6.covarianceforecasting import m6_cov
from precise.skaters.covarianceutil.covfunctions import affine_shrink, nearest_pos_def


def what_pctl_number_of(x, a, pctls=[20,40,60,80]):
    return np.argmax(np.sign(np.append(np.percentile(x, pctls), np.inf) - a))

def mvn_quintile_probabilities(sgma, n_samples):
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
    df_cov = pd.DataFrame(columns=tickers, index=tickers, data=sgma)
    return df, df_cov


def m6_entry(interval='d',n_dim=100, n_samples=5000, n_obs=200):
    """
           Example of generating an M6 Entry
           pip install PyPortfolioOpt
    """
    from pypfopt.efficient_frontier import EfficientFrontier
    df_prob, df_cov = m6_probabilities(interval=interval, n_dim=n_dim, n_samples=n_samples, n_obs=n_obs)
    cov = df_cov.values
    phi = 1.1 + 0.1 * np.random.rand()
    lbmda = 0.03 * np.random.randn()
    cov = affine_shrink(cov, phi=phi, lmbd=lbmda)
    cov = nearest_pos_def(cov)
    n_dim = len(df_cov.index)
    mu = np.zeros(n_dim)
    ef = EfficientFrontier(mu, cov)
    weights = ef.max_quadratic_utility()
    entry = df_prob.copy()
    entry['Decision'] = [round(weights[i], 5) for i in range(n_dim)]
    entry.rename(inplace=True, columns={'0': 'Rank1', '1': 'Rank2', '2': 'Rank3', '3': 'Rank4', '4': 'Rank5'})
    return entry


if __name__=='__main__':
    df = m6_entry()
    df.to_csv('m6_entry.csv')




