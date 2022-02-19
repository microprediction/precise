import pandas as pd
import numpy as np
import random


def random_cached_equity_dense(k, n_obs, n_dim=10, as_frame=False, **ignore):
    """
         Log price differences without missing values
         :param k - days

    """
    pd.options.mode.chained_assignment = None
    df = _sparse_cached_equity(k=k)
    n_samples = len(df.index)
    assert n_samples>n_obs
    n_start = random.choice(range(n_samples-n_obs))
    n_end = n_start + n_obs
    df_sub = df[n_start:n_end]
    df_sub.dropna(how='any', inplace=True, axis=1)
    df_sub.drop(df.columns[0], inplace=True, axis=1)
    size = min(len(df_sub.columns),n_dim)
    selected = np.random.choice(df_sub.columns, size=size, replace=False)
    df_some = df_sub[selected]
    return df_some if as_frame else df_some.values


def _sparse_cached_equity(k=1):
    """ Retrieve daily or less frequent price changes
    :param k:  difference measured in business days
    :returns   pd.DataFrame with NaNs
    """
    import ssl

    # creates an unverified certificate with ssl even without certificate
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    CSV ='https://raw.githubusercontent.com/microprediction/precisedata/main/stocks/log_price_diff_K_part_N.csv'
    dfs = [ pd.read_csv(CSV.replace('K',str(k)).replace('N',str(part)) ) for part in list(range(1,4)) ]
    df_merged = pd.concat(dfs,axis=1)
    return df_merged



if __name__=='__main__':
    df = _sparse_cached_equity(k=1)
    print(df[:3])
    dg = random_cached_equity_dense(k=1, n_obs=50, as_frame=True)
    print(dg)