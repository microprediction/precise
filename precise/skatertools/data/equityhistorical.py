import pandas as pd
import random


def get_log_price_diff(k=1):
    """ Daily or less frequent price changes
    :param k:  difference measured in business days
    :returns   pd.DataFrame with NaNs
    """
    CSV ='https://raw.githubusercontent.com/microprediction/precisedata/main/stocks/log_price_diff_K_part_N.csv'
    dfs = [ pd.read_csv(CSV.replace('K',str(k)).replace('N',str(part)) ) for part in list(range(1,4)) ]
    df_merged = pd.concat(dfs,axis=1)
    return df_merged


def get_random_dense_log_price_diff(k,n_obs,**ignore):
    df = get_log_price_diff(k=k)
    n_samples = len(df.index)
    assert n_samples>n_obs
    n_start = random.choice(range(n_samples-n_obs))
    n_end = n_start + n_obs
    df_sub = df[n_start:n_end]
    df_sub.dropna(how='any', inplace=True, axis=1)
    return df_sub


if __name__=='__main__':
    df = get_log_price_diff(k=1)
    print(df[:3])
    dg = get_random_dense_log_price_diff(k=1,n_obs=50)
    print(dg)