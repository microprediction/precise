import pandas_datareader.data as web
import pandas as pd
import time
from functools import lru_cache
import numpy as np


@lru_cache(maxsize=500)
def get_prices(ticker,n_obs,interval):
    return web.get_data_yahoo(ticker, interval=interval)[-n_obs - 1:]['Close'].values


def random_m6_returns(n_dim=10, n_obs:int=60, verbose=True, interval='m', etf=0, **ignore):
    """
        Use portfolio for M6 competition
    """
    constituents = pd.read_csv('https://raw.githubusercontent.com/microprediction/m6/main/data/official/M6_Universe.csv')
    if etf:
        tickers = constituents['symbol']
    else:
        tickers = constituents['symbol'][50:]
    return random_equity_returns(all_tickers=tickers, n_dim=n_dim, n_obs=n_obs, verbose=verbose, interval=interval)


def random_equity_returns(all_tickers, n_dim=10, n_obs:int=60, verbose=True, interval='m', **ignore):
    """ Get return series
    :param n_dim:            Number of assets
    :param n_obs:
    :param interval: 'd' or 'm'
    :return:
    """
    assert 2*n_dim<=len(all_tickers)
    if interval=='m':
        assert n_obs<=60,'too many observations for monthly'

    tickers = list(np.random.choice(all_tickers, n_dim * 2, replace=False))
    prices = list()
    while (len(prices)<n_dim) and len(tickers):
        ticker = tickers.pop()
        data = []
        try:
            data = get_prices(ticker=ticker,n_obs=n_obs, interval=interval)
            if len(data)==n_obs+1:
                prices.append(np.diff(np.log(data)))
            if verbose:
                print('Got '+ticker+' len '+str(len(data)))
        except Exception as e:
            print('Failure getting '+ticker)
            time.sleep(1)
    prices_transposed = list(map(list, zip(*prices)))
    return prices_transposed



if __name__=='__main__':
    import numpy as np
    from pprint import pprint
    a = random_m6_returns(n_dim=3, n_obs=60, etf=1)
    c = np.corrcoef(np.array(a),rowvar=False)
    pprint(c)