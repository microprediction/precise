import pandas_datareader.data as pdr
import yfinance as yf


import pandas as pd
import time
from functools import lru_cache
import numpy as np
import time

@lru_cache(maxsize=500)
def get_prices(ticker,n_obs,interval, max_attempts=10):
    if interval=='m':
        interval = '1mo'

    print('Getting '+ticker)
    time.sleep(5)
    success = False
    attempts = 0
    while not success:
        try:
            data = pdr.get_data_yahoo(ticker, interval=interval)[-n_obs - 1:]['Close'].values
            success = True
        except Exception as e:
            print(str(e))
            print('backing off')
            time.sleep(10)
            attempts += 1
            if attempts>=max_attempts:
                raise ValueError
    return data



def live_equity_returns(tickers, n_obs=60, interval='1d', k=1):
    df = pd.DataFrame()
    for ticker in tickers:
        try:
            data = get_prices(ticker=ticker, n_obs=n_obs, interval=interval)
            assert len(data)==n_obs+1
            values = list(np.diff(np.log(data),k))[::k]
            df[ticker] = values
        except:
            pass
    return df


def live_veteran_etf_data(interval='1d',k=1):
    from precise.skatertools.data.etflists import VETERAN_NON_BOND_ETFS
    n_obs = 60 if interval=='m' else 250
    df = live_equity_returns(tickers=VETERAN_NON_BOND_ETFS, n_obs=n_obs, interval=interval, k=k)
    return df


def random_m6_returns(n_dim=10, n_obs:int=60, verbose=True, interval='1d', etf=0, **ignore):
    """
        Use portfolio for M6 competition
    """
    constituents = pd.read_csv('https://raw.githubusercontent.com/microprediction/m6/main/data/official/M6_Universe.csv')
    if etf==0:
        tickers = constituents['symbol'][:50]
    elif etf>0:
        tickers = constituents['symbol']
    else:
        tickers = constituents['symbol'][50:]
    return random_equity_returns(all_tickers=tickers, n_dim=n_dim, n_obs=n_obs, verbose=verbose, interval=interval)


def random_rdps_returns(n_dim=10, n_obs:int=60, verbose=True, interval='1d', etf=1, **ignore):
    """
        Leave one-out sectors by default
    """
    from getjson import getjson
    rdps_tickers = getjson('https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/rdpstickers.json')
    tickers = list(rdps_tickers.values())
    return random_equity_returns(all_tickers=tickers, n_dim=n_dim, n_obs=n_obs, verbose=verbose, interval=interval)



def all_m6_returns(n_obs:int=60, verbose=True, interval='1d', etf=0, implied=0, **ignore):
    n_buffer = np.random.choice([20,40,60,80,100,120,140])
    constituents = pd.read_csv(
        'https://raw.githubusercontent.com/microprediction/m6/main/data/official/M6_Universe.csv')
    if etf == 0:
        tickers = constituents['symbol'][:50]
    elif etf > 0:
        tickers = constituents['symbol']
    else:
        tickers = constituents['symbol'][50:]
    xs = get_equity_returns(tickers=tickers, n_obs=n_obs+n_buffer, verbose=verbose, interval=interval, implied=implied)

    return xs[:-n_buffer]


def get_equity_returns(tickers, n_obs:int=60, verbose=True, interval='5d', implied=0, **ignore):
    """ Get return series for those of minimum length desired
    :param n_dim:            Number of assets
    :param n_obs:
    :param interval: 'd' or 'm'
    :return: prices NOT necessarily corresponding to all_tickers
    """
    if interval=='m':
        interval='1mo'
    if interval == 'd':
        interval = '1d'

    if interval=='1mo':
        assert n_obs<=60,'too many observations for monthly'

    prices = list()
    for ticker in tickers:
        data = []
        try:
            data = get_prices(ticker=ticker,n_obs=n_obs, interval=interval)
            if implied:
                from precise.skatervaluation.battledata.m6implied import all_vols
                vol = all_vols.get(ticker)
                if vol is None:
                    data = []
                else:
                    data = np.array(data)/vol

            if len(data)==n_obs+1:
                prices.append(np.diff(np.log(data)))
                if verbose:
                    print('Got '+ticker+' len '+str(len(data)))
            else:
                if verbose:
                    print('Skipping '+ticker+' len '+str(len(data)))
        except Exception as e:
            print('Failure getting '+ticker)
            time.sleep(1)

    prices_transposed = list(map(list, zip(*prices)))
    return np.array(prices_transposed)


def random_equity_returns(all_tickers, n_dim=10, n_obs:int=60, verbose=True, interval='1d', **ignore):
    """ Get return series
    :param n_dim:            Number of assets desired, but may return less
    :param n_obs:
    :param interval: '1d' or '1mo'
    :return: prices NOT necessarily corresponding to all_tickers
    """
    if interval=='1mo':
        assert n_obs<=60,'too many observations for monthly'
    n_take = min(len(all_tickers),2*n_dim)
    tickers = list(np.random.choice(all_tickers, n_take, replace=False))
    unique_tickers = list(set(tickers))
    if len(unique_tickers)<n_dim:
        n_dim = len(unique_tickers)
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
    return np.array(prices_transposed)



if __name__=='__main__':
    import numpy as np
    from pprint import pprint
    a = random_rdps_returns(n_dim=3, n_obs=60, etf=1)
    c = np.corrcoef(np.array(a),rowvar=False)
    pprint(c)