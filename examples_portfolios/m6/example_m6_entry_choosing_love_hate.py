from precise.skatertools.m6.competition import m6_competition_entry, m6_dump
from precise.whereami import M6_EXAMPLES
import os
import time

# Example of creating an M6 Competition entry with some loved and hated tickers

if __name__=='__main__':
    love = ['IAU']         # Peruse https://github.com/microprediction/m6/blob/main/data/official/M6_Universe.csv
    hate = ['REET','XLB']  # Not investment advice
    df = m6_competition_entry(love=love, hate=hate)
    timestamped_csv_file = os.path.join(M6_EXAMPLES, 'full', 'm6_' + time.strftime("%Y%m%d-%H%M%S") + '.csv')
    m6_dump(df=df,file_name=timestamped_csv_file)