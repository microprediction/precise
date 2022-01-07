import pandas as pd
stocks = ['FB','GOOG','APPL']
from precise.universe import sp_tickers
import quantstats as qs
import datetime
import numpy as np

def normalize(xs):
    return [ xi/sum(xs) for xi in xs]

def test_sp():
    n=5
    tickers = sp_tickers()[:n]
    df = pd.DataFrame(columns=tickers)
    print(tickers)
    for ticker in tickers:
        df[ticker] = qs.utils.download_returns(ticker=ticker, period='2y').values[1:]
    n_samples = int(len(df)/2)
    print({'len':len(df)})
    c1 = df[1:250].cov()
    c1inv = np.linalg.pinv(c1.values)
    p1 = pd.DataFrame(c1inv, c1.columns, c1.index)
    c2 = df[250:].cov()
    c2inv = np.linalg.pinv(c2.values)
    p2 = pd.DataFrame(c2inv, c2.columns, c2.index)
    print(c1/c2)
    print(p1)
    print(p2)
    p1_raw = np.squeeze(np.matmul(c1inv),np.ones(shape=(n,1)))
    portfolio1 = p1_raw/sum(p1_raw)
    print(portfolio1)
    p2_raw = np.squeeze(np.matmul(c2inv, np.ones(shape=(n, 1))))
    portfolio2 = p2_raw/sum(p2_raw)
    print(portfolio2)
    returns = np.matmul( df[250:].values, portfolio1 )



if __name__=='__main__':
    test_sp()