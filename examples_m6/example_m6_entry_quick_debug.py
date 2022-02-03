from precise.skatertools.m6.competition import m6_competition_entry, m6_dump
from precise.whereami import M6_EXAMPLES
import os
import time
from pprint import pprint

# Example of creating an M6 Competition entry using less than the full set of tickers

if __name__=='__main__':
    df = m6_competition_entry(n_dim=10)
    pprint(df)
