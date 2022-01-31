

if __name__=='__main__':
    from precise.skatertools.m6.quintileprobabilities import m6_entry
    df = m6_entry()
    df.to_csv('m6.csv')