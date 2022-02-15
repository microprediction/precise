# Miscellaneous lists OF ETFS for paper

SOFI_ETFS = ['SFY', 'SFYX']
VANGUARD_ETFS = ['BND', 'VCIT', 'VOO', 'VTI', 'VUG', 'VV', 'VTV', 'VIG', 'VO', 'VB']  # <-- Those with fee <= 5bps
SCHWAB_ETFS = ['SCHB', 'SCHK', 'SCHX', 'SCHG', 'SCHV', 'SCHM', 'SCHA', 'SCHF', 'SCHC', 'SCHY', 'SCHE', 'SCHP', 'SCHR',
               'SCHJ', 'SCHI', 'SCHQ']
INVESCO_ETFS = ['SOXQ', 'IBBQ', 'RPV']
FACTOR_ETFS = ['PDP', 'SDOG', 'SPYG', 'SPLV', 'DGRW']
MISC_ETFS = ['RSP', 'NOBL', 'PGX', 'BKNL', 'FNDE', 'CWB', 'RPG', 'GNR', 'SGOL', 'XLG', 'CWI', 'HYS', 'GXC',
             'VOTE', 'GBUG']

ETFS = list(set(SOFI_ETFS + VANGUARD_ETFS + SCHWAB_ETFS + INVESCO_ETFS + FACTOR_ETFS + MISC_ETFS))

# A few with decent history via yahoo datareader:
VETERAN_NON_BOND_ETFS = ['RPG', 'SCHC', 'SCHV', 'VUG', 'SDOG', 'VOO', 'DGRW', 'CWB', 'CWI', 'SCHA', 'VTV', 'VIG',
                'NOBL', 'SCHG', 'SCHX', 'SPLV', 'VO', 'VTI', 'FNDE', 'SCHM', 'VV', 'XLG', 'GXC',
                'PDP', 'GNR', 'SPYG', 'RSP', 'RPV',  'SCHE', 'SCHF', 'SCHB', 'VB']
VETERAN_BOND_ETFS = ['HYS', 'BND','SCHP', 'SCHR','PGX','VCIT']
VETERAN_ETFS = VETERAN_NON_BOND_ETFS + VETERAN_BOND_ETFS

VETERAN_VOL = {'BND': 6,
               'CWB': 24,
               'CWI': 17,
               'DGRW': 22,
               'FNDE': 17,
               'GNR': 17,
               'GXC': 23.5,
               'HYS': 9,
               'NOBL': 16,
               'PDP': 27,
               'PGX': 17,
               'RPG': 34,
               'RPV': 29,
               'RSP': 23,
               'SCHA': 27,
               'SCHB': 17,
               'SCHC': 17,
               'SCHE': 21,
               'SCHF': 19,
               'SCHG': 32,
               'SCHM': 25,
               'SCHP': 9.3,
               'SCHR': 4.8,
               'SCHV': 21,
               'SCHX': 22,
               'SDOG': 17,
               'SGOL': 15,
               'SPLV': 20,
               'SPYG': 30,
               'VB': 26,
               'VCIT': 7,
               'VIG': 20,
               'VO': 25,
               'VOO': 25,
               'VTI': 25,
               'VTV': 20,
               'VUG': 30,
               'VV': 26,
               'XLG': 27}


def veterans():
    from precise.skatertools.data.equitylive import get_prices
    import time
    veteran_etfs = list()
    for etf in ETFS:
        try:
            data = get_prices(ticker=etf, interval='m', n_obs=60, max_attempts=1)
            n = len(data)
            print((etf, str(n)))
            if n == 61:
                veteran_etfs.append(etf)
            time.sleep(5)
        except:
            print('No data for ' + etf)
            pass
    return veteran_etfs


if __name__ == '__main__':
    print(len(VETERAN_ETFS))
    print([missing for missing in VETERAN_ETFS if not missing in VETERAN_VOL])
