import numpy as np
from precise.skatertools.data.equitylive import get_prices
import pandas as pd
from pprint import pprint
from precise.skaters.covariance.runemp import run_emp_pcov_d0


def m6_data(interval='d', n_dim=100, n_obs=300):
    constituents = pd.read_csv(
        'https://raw.githubusercontent.com/microprediction/m6/main/data/official/M6_Universe.csv')[:n_dim]
    tickers = constituents['symbol'].values
    if (interval=='m') and (n_obs>60):
        print('Too many obs, switching to daily ')
        interval = 'd'
    df = pd.DataFrame(columns=tickers)
    for ticker in tickers:
        closing_prices = get_prices(ticker=ticker, n_obs=n_obs+1, interval=interval)
        while len(closing_prices) < n_obs+1:
            closing_prices = list(closing_prices) + list(closing_prices)
        closing_prices = closing_prices[-n_obs:]
        df[ticker] = np.diff(np.log(closing_prices))
    return df


def m6_cov(f=None, interval='d', n_dim=100, n_obs=300):
    """ Use any skater to estimate daily (by default) covariance
    :param f: cov skater
    :return:
    """
    if f is None:
        f = run_emp_pcov_d0
    df = m6_data(interval=interval, n_dim=n_dim, n_obs=n_obs)
    tickers = list(df.columns)

    s = {}
    for y in df.values:
        x_mean, x_cov, s = f(s=s, y=y)
    return pd.DataFrame(index=tickers, columns=tickers, data=x_cov)


def m6_corr(f=None, n_dim=100, interval='d',n_obs=300):
    from precise.skaters.covarianceutil.datafunctions import cov_to_corrcoef
    covdf = m6_cov(f=f, n_dim=n_dim, interval=interval, n_obs=n_obs)
    tickers = list(covdf.columns)
    corr = cov_to_corrcoef(covdf.values)
    dfc = pd.DataFrame(index=tickers, columns=tickers, data=corr)
    return dfc


if __name__=='__main__':
    from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r01 as f
    pprint(m6_corr(interval='d',n_dim=4,f=f))
