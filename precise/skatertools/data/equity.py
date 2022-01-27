

import pandas_datareader.data as web
import pandas as pd
import numpy as np
import time
from functools import lru_cache


@lru_cache(maxsize=500)
def get_prices(ticker,n_obs,interval):
    return web.get_data_yahoo(ticker, interval=interval)[-n_obs - 1:]['Close'].values


def random_m6_returns(n_dim=10, n_obs:int=60, verbose=True, interval='m', **ignore):
    """
    :param n_dim:
    :param n_obs:
    :param verbose:
    :param interval: 'd' or 'm'
    :return:
    """
    assert n_dim<=25
    if interval=='m':
        assert n_obs<=60
    constituents = pd.read_csv('https://raw.githubusercontent.com/microprediction/m6/main/data/official/M6_Universe.csv')
    stock_tickers_repeatd = constituents['symbol'][:50]
    tickers = list(np.random.choice(stock_tickers_repeatd,n_dim*2, replace=False))
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
    a = random_m6_returns(n_dim=3, n_obs=60)
    c = np.corrcoef(np.array(a),rowvar=False)
    pprint(c)