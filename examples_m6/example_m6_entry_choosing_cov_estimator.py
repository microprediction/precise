from precise.skatertools.m6.competition import m6_competition_entry, m6_dump
from precise.whereami import M6_EXAMPLES
import os
import time

# Example of creating an M6 Competition entry and choosing a method of predicting covariancecomparisonutil

if __name__=='__main__':
    from precise.skaters.covariance.bufsk import buf_sk_oas_pcov_d0_n100 as f   # Sklearn's Oracle Approx implementation
    df = m6_competition_entry(f=f)
    timestamped_csv_file = os.path.join(M6_EXAMPLES,'full','m6_'+time.strftime("%Y%m%d-%H%M%S")+'.csv')
    m6_dump(df=df,file_name=timestamped_csv_file)