from precise.skaters.portfolioutil.portfunctions import portfolio_variance
import numpy as np
import pandas as pd


def equity_portfolio_variance_rankings(ports, n_dim=10, n_obs = 300, interval='d', etf=1, as_frame=True):
    from precise.skatertools.data.equity import random_m6_returns
    data = random_m6_returns(n_dim=n_dim, n_obs=n_obs, verbose = False, interval = interval, etf = etf)
    t_obs = int(0.5*n_obs)
    test_cov = np.cov(data[:t_obs] ,rowvar=False)
    train_cov = np.cov(data[t_obs:], rowvar=False)
    return portfolio_variance_rankings(cov_test=test_cov, ports=ports, cov_train=train_cov, as_frame=as_frame )


def portfolio_variance_rankings(cov_train, ports, cov_test=None, as_frame=True):
    """  Really crude comparison with single train/test

    :param cov_train:    Training cov matrix
    :param ports:        List of portfolio methods
    :param cov_test:
    :param as_frame:
    :return:
    """

    if cov_test is None:
        cov_test = cov_train
    rankings = list()
    for port in ports:
        w = port(cov_train)
        in_var = portfolio_variance(cov=cov_train, w=w)
        out_var = portfolio_variance(cov=cov_test, w=w)
        rankings.append((port.__name__, in_var, out_var))
    leaderboard = sorted(rankings, key=lambda t :t[2])
    if as_frame:
        bestout = leaderboard[0][2]
        df = pd.DataFrame(columns=['method' ,'invar' ,'outvar'] ,data=leaderboard)
        df['out sample relative'] = df['outvar']/bestout
        return df
    else:
        return leaderboard


