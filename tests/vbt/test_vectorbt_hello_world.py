import numpy as np
import pandas as pd
from datetime import datetime
import vectorbt as vbt


def test_much():
    assert True


def test_hello():
    start = '2019-01-01 UTC'  # crypto is in UTC
    end = '2020-01-01 UTC'
    btc_price = vbt.YFData.download('BTC-USD', start=start, end=end).get('Close')
    fast_ma = vbt.MA.run(btc_price, 10, short_name='fast')
    slow_ma = vbt.MA.run(btc_price, 20, short_name='slow')
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)
    pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
    pf.total_return()


if __name__=='__main__':
    test_hello()