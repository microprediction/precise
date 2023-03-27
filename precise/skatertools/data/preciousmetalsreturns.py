import pandas as pd
from precise.whereami import ROOT
import os
import numpy as np
from precise.skatertools.data.equityhistorical import random_cached_equity_dense


def precious_metals_returns():
    CSV = os.path.join(ROOT, 'private_examples', 'precious_metals.csv')
    try:
        df = pd.read_csv(CSV,index_col=None)
        driver_cols = [c for c in df.columns if not 'date' in c and not 's500' in c]
        for c in driver_cols:
            df[c] = df[c] - df['s500']
        xs = 0.01 * df[driver_cols].values
        return xs
    except Exception as e:
        print(e)
        return random_cached_equity_dense(k=1, n_obs=5000, n_dim=10, as_frame=False)





if __name__=='__main__':
    print(precious_metals_returns()[:2])