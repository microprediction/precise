from precise.skatertools.m6.competition import m6_competition_entry, m6_dump
from precise.whereami import M6_EXAMPLES
import os
import time

# Example of creating an M6 Competition entry using random choice of cov estimation and port construction


def test_m6_entry():
    love = ['IAU']  # Peruse https://github.com/microprediction/m6/blob/main/data/official/M6_Universe.csv
    hate = ['REET', 'XLB']  # Not investment advice
    from precise.skaters.portfoliostatic.hrpport import hrp_unit_unit_s5_port as port
    from precise.skaters.covariance.bufsk import buf_sk_oas_pcov_d0_n100 as f  # Sklearn's Oracle Approx implementation
    df = m6_competition_entry(n_dim=5,f=f, love=love, hate=hate, intensity=0.5, port=port)
    timestamped_csv_file = os.path.join(M6_EXAMPLES,'partial','m6_'+time.strftime("%Y%m%d-%H%M%S")+'.csv')
    m6_dump(df=df,file_name=timestamped_csv_file)