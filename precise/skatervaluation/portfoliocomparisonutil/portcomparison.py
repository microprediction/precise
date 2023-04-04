from precise.skaters.portfolioutil.portfunctions import portfolio_variance
import numpy as np
import pandas as pd
from collections import Counter
from pprint import pprint
from precise.skaters.covarianceutil.covrandom import random_known_cov
from momentum import kurtosis_init, kurtosis_update
import time

from precise.skaters.covarianceutil.covrandom import random_factor_cov


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


def rdps_portfolio_variance_points_race(n_iter=100,n_top=50, **kwargs):
    return points_race(n_iter=n_iter, n_top=n_top, ranker=rdps_etf_variance_rankings, ranker_kwargs=kwargs)


def equity_portfolio_correlation_points_race(n_iter=100,n_top=50, **kwargs):
    return points_race(n_iter=n_iter, n_top=n_top, ranker=m6_equity_portfolio_correlation_rankings, ranker_kwargs=kwargs)


def rdps_etf_variance_rankings(ports, n_dim=10, n_obs = 300, k=1, as_frame=True, n_iter=10):
    """
        Quick and dirty leave one-out
    """
    from precise.skatertools.data.equitylive import random_rdps_returns
    data = random_rdps_returns(n_dim=n_dim, n_obs=n_obs, verbose = False, k=k)
    t_obs = int(0.75*n_obs)
    test_cov = np.cov(data[:t_obs] ,rowvar=False)
    train_cov = np.cov(data[t_obs:], rowvar=False)
    return portfolio_variance_rankings(cov_test=test_cov, ports=ports, cov_train=train_cov, as_frame=as_frame, n_iter=n_iter )


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


def m6_equity_portfolio_variance_rankings(ports, n_dim=10, n_obs = 300, interval='1d', etf=1, as_frame=True, n_iter=10):
    """
        Quick and dirty
    """
    from precise.skatertools.data.equitylive import random_m6_returns
    data = random_m6_returns(n_dim=n_dim, n_obs=n_obs, verbose = False, interval = interval, etf = etf)
    t_obs = int(0.5*n_obs)
    test_cov = np.cov(data[:t_obs] ,rowvar=False)
    train_cov = np.cov(data[t_obs:], rowvar=False)
    return portfolio_variance_rankings(cov_test=test_cov, ports=ports, cov_train=train_cov, as_frame=as_frame, n_iter=n_iter )


def m6_equity_portfolio_correlation_rankings(ports, n_dim=10, n_obs = 300, interval='1d', etf=1, as_frame=True):
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


def port_sample_var(ports, cov, n_anchor, n_observed, n_true, show_progress=True, max_time=10*60):
    """ Judge and rank by simulated portfolio variance when ...
            anchor is samples from cov
                 true is samples from anchor
                      observed is samples from true
    :param ports:
    :param cov:
    :param n_draws:
    :param n_true:
    :return:
    """
    cov = random_factor_cov(n_dim=np.shape(cov)[0])
    moments = port_kurtosis(ports=ports, seed_cov=cov, max_time=max_time, n_anchor=n_anchor, n_observed=n_observed,
                            n_true=n_true, metric='mean', show_progress=show_progress)
    return sorted( moments.items(), key=lambda x: x[1], reverse=False)


def port_kurtosis(ports, seed_cov, n_observed, n_anchor=None, n_true=None,
                  metric=None, show_progress=True, port_kwargs=None,
                  max_time=5*60, **ignore):
    """
         Sample true and observed cov matrices, and compute out of sample portfolio var

    :param ports:     List of port functions
    :param seed_cov:  Covariance used to generate both true and observed cov
    :param n_true:    Number of samples used to generate random true and observed cov from anchor, or None
    :param n_anchor:  Number of samples used to generate random anchor from cov, or None
    :param n_observed Number of samples used to estimate corr matrices
    :param metric:    If supplied, will return
    :param max_time   Seconds to run for
    :return:
    """
    if port_kwargs is None:
        port_kwargs = {}

    def covrnd():
        return seed_cov

    return portfolio_variance_comparison(ports=ports, covrnd=covrnd, n_anchor=n_anchor,
                                   n_observed=n_observed, n_true=n_true, metric=metric, show_progress=show_progress,
                                         port_kwargs=port_kwargs, max_time=max_time)



def portfolio_variance_comparison(ports, covrnd, n_observed, max_time=5*60, n_anchor=None, n_true=None,
                                  metric=None, show_progress=True, port_kwargs=None):
    """
         Sample true and observed cov matrices, and compute out of sample portfolio var

    :param ports:     List of port functions
    :param covrnd:    Function returning a random covariancecomparisonutil matrix
    :param n_draws:   Number of outer iterations
    :param n_true:    Number of samples used to generate random true and observed cov from anchor, or None
    :param n_anchor:  Number of samples used to generate random anchor from cov
    :param n_observed Number of samples used to estimate corr matrices
    :param metric:    If supplied, will return
    :return:
    """
    if port_kwargs is None:
        port_kwargs = {}

    run_start_time = time.time()

    last_update_time = time.time()-60
    moments = dict([(port.__name__, kurtosis_init()) for port in ports])
    draw_no = 0
    while time.time()-run_start_time<max_time:
        draw_no += 1
        cov = covrnd()
        if n_anchor is None:
            anchor_cov = np.copy(cov)
        else:
            anchor_cov = random_known_cov(cov=cov, n_samples=n_anchor)
        if n_true is None:
            true_cov = np.copy(anchor_cov)
        else:
            true_cov = random_known_cov(cov=anchor_cov, n_samples=n_true)
        obs_cov = random_known_cov(cov=true_cov, n_samples=n_observed)
        for port in ports:
            w = port(cov=np.copy(obs_cov),**port_kwargs)
            if abs(np.sum(w)-1)>0.01:
                print('weight did not sum to unity')
            pv = portfolio_variance(w=w, cov=true_cov)
            if abs(pv)<0.001:
                print('hmmm')
            moments[port.__name__] = kurtosis_update(moments[port.__name__], pv )
        if show_progress:
            if time.time()-last_update_time>20:
                import math
                the_means = [(pn, m.get('mean'), m.get('std')/math.sqrt(1+draw_no)) for pn, m in moments.items()]
                pprint(sorted(the_means, key=lambda x: x[1]))
                last_update_time = time.time()

    if metric is not None:
        return dict([ (pn,m.get(metric)) for pn,m in moments.items() ])
    else:
        return moments


if __name__=='__main__':
    from precise.skaters.portfoliostatic.rpport import RP_LONG_PORT
    from precise.skaters.portfoliostatic.schurport import SCHUR_LONG_PORT
    from precise.skaters.portfoliostatic.hrpport import HRP_LONG_PORT
    ports = RP_LONG_PORT + SCHUR_LONG_PORT + HRP_LONG_PORT
    #rdps_portfolio_variance_points_race(n_iter=500,n_top=50, n_obs =120, ports=ports)
    stock_portfolio_variance_points_race(n_iter=500,n_top=50, n_obs =200, ports=ports, n_dim=100)