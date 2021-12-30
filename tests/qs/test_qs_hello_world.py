import quantstats as qs


def test_hello_quantstats():
    qs.extend_pandas()
    stock = qs.utils.download_returns('FB')
    qs.stats.sharpe(stock)
    

if __name__=='__main__':
    test_hello_quantstats()