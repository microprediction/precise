from precise.skatertools.m6.competition import m6_competition_entry, m6_dump
from precise.whereami import M6_EXAMPLES
import os
import time


if __name__=='__main__':
    n_dim = 100 # <-- 100 for real thing, less for testing
    df = m6_competition_entry(n_dim=n_dim)
    classification = 'full' if (n_dim==100) else 'partial'
    timestamped_csv_file = os.path.join(M6_EXAMPLES,classification,'m6_'+time.strftime("%Y%m%d-%H%M%S")+'.csv')
    m6_dump(df=df,file_name=timestamped_csv_file)