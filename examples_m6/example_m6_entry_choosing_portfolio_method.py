from precise.skatertools.m6.competition import m6_competition_entry, m6_dump
from precise.whereami import M6_EXAMPLES
import os
import time

# Example of creating an M6 Competition entry and choosing a method of constructing a portfolio

if __name__=='__main__':
    from precise.skaters.portfolioutil.parity import prc_hrp_diag_5 as port  # Hierarchical risk-parity
    df = m6_competition_entry(port=port)
    timestamped_csv_file = os.path.join(M6_EXAMPLES,'full','m6_'+time.strftime("%Y%m%d-%H%M%S")+'.csv')
    m6_dump(df=df,file_name=timestamped_csv_file)