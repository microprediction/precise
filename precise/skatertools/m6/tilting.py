
import numpy as np
import pandas as pd


def affection_tilt(covdf:pd.DataFrame, love:[str]=None, hate:[str]=None, intensity=1.0):
    """ Convert list of tickers loved and hated into relative means
    :param covdf:   covariance pandas dataframe with tickers as columns and index
    :param love:
    :param hate:
    :return:
    """
    mean_var = np.mean(np.diag(covdf.values))
    tickers = list(covdf.columns)
    n_dim = len(tickers)

    mu = np.zeros(n_dim)
    if love is not None:
        for ticker in love:
            if ticker in tickers:
                mu[tickers.index(ticker)] = intensity * 0.1 * mean_var / 2

    if hate is not None:
        for ticker in hate:
            if ticker in tickers:
                mu[tickers.index(ticker)] = -intensity * 0.1 * mean_var / 2

    return mu