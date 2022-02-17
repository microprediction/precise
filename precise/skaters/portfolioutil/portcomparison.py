from precise.skaters.portfolioutil.portfunctions import portfolio_variance
import numpy as np
import pandas as pd
from collections import Counter
from pprint import pprint


def points_race( ranker, ranker_kwargs, n_iter=100, n_top=20):
    c = Counter()
    for _ in range(n_iter):
        rankings = ranker(as_frame=False, **ranker_kwargs)
        points = [ (port_name, max(len(rankings)-k,0) ) for k,(port_name,_,_) in enumerate(rankings) ]
        c.update(dict(points))
        pprint(c.most_common(n=n_top))
    return c


def stock_portfolio_variance_points_race(n_iter=100,n_top=50, **kwargs):
    return points_race(n_iter=n_iter, n_top=n_top, ranker=stock_portfolio_variance_rankings, ranker_kwargs=kwargs)


def equity_portfolio_variance_points_race(n_iter=100,n_top=50, **kwargs):
    return points_race(n_iter=n_iter, n_top=n_top, ranker=m6_equity_portfolio_variance_rankings, ranker_kwargs=kwargs)


def equity_portfolio_correlation_points_race(n_iter=100,n_top=50, **kwargs):
    return points_race(n_iter=n_iter, n_top=n_top, ranker=m6_equity_portfolio_correlation_rankings, ranker_kwargs=kwargs)


def stock_portfolio_variance_rankings(ports, n_dim=10, n_obs = 300, k=1, as_frame=True, n_iter=10):
    """
        Quick and dirty
    """
    from precise.skatertools.data.equityhistorical import random_cached_equity_dense
    data = random_cached_equity_dense(n_dim=n_dim, n_obs=n_obs, verbose = False, k=k)
    t_obs = int(0.75*n_obs)
    test_cov = np.cov(data[:t_obs] ,rowvar=False)
    train_cov = np.cov(data[t_obs:], rowvar=False)
    return portfolio_variance_rankings(cov_test=test_cov, ports=ports, cov_train=train_cov, as_frame=as_frame, n_iter=n_iter )


def m6_equity_portfolio_variance_rankings(ports, n_dim=10, n_obs = 300, interval='d', etf=1, as_frame=True, n_iter=10):
    """
        Quick and dirty
    """
    from precise.skatertools.data.equitylive import random_m6_returns
    data = random_m6_returns(n_dim=n_dim, n_obs=n_obs, verbose = False, interval = interval, etf = etf)
    t_obs = int(0.5*n_obs)
    test_cov = np.cov(data[:t_obs] ,rowvar=False)
    train_cov = np.cov(data[t_obs:], rowvar=False)
    return portfolio_variance_rankings(cov_test=test_cov, ports=ports, cov_train=train_cov, as_frame=as_frame, n_iter=n_iter )


def m6_equity_portfolio_correlation_rankings(ports, n_dim=10, n_obs = 300, interval='d', etf=1, as_frame=True):
    """
        Quick and dirty comparison using empirical corrcoef for cov
    """
    from precise.skatertools.data.equitylive import random_m6_returns
    data = random_m6_returns(n_dim=n_dim, n_obs=n_obs, verbose = False, interval = interval, etf = etf)
    t_obs = int(0.666*n_obs)
    test_cov = np.corrcoef(data[:t_obs] ,rowvar=False)
    train_cov_gen = np.corrcoef(data[t_obs:], rowvar=False)
    n = np.shape(data)[1]
    ys = np.random.multivariate_normal(mean=np.zeros(n), cov=train_cov_gen, size=50 )
    train_cov = np.cov(ys, rowvar=False)

    return portfolio_variance_rankings(cov_test=test_cov, ports=ports, cov_train=train_cov, as_frame=as_frame )


def portfolio_variance_rankings(cov_train, ports, cov_test=None, as_frame=True, n_iter=1):
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
        try:
            in_var = portfolio_variance(cov=cov_train, w=w)
            out_var = portfolio_variance(cov=cov_test, w=w)
        except ValueError:
            print('portfolio may be wrong shape, or cov_tain, cov_test')
            raise
        rankings.append((port.__name__, in_var, out_var))
    leaderboard = sorted(rankings, key=lambda t :t[2])

    if as_frame:
        bestout = leaderboard[0][2]
        df = pd.DataFrame(columns=['method' ,'invar' ,'outvar'] ,data=leaderboard)
        df['out sample relative'] = df['outvar']/bestout
        return df
    else:
        return leaderboard


