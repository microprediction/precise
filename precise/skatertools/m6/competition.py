from pprint import pprint
from precise.skaters.covarianceutil.covfunctions import affine_shrink, nearest_pos_def
from precise.skaters.portfoliostatic.allstaticport import random_port, PORT
from precise.skaters.covariance.allcovskaters import random_cov_skater, cov_skater_manifest
from precise.skatertools.m6.quintileprobabilities import m6_probabilities
from precise.skatertools.m6.tilting import affection_tilt

# Demonstrates the creation of an entry in the M6 contest
#
#   1. Pick a cov estimator (i.e. a "cov skater"), if you wish
#   2. Pick a portfolio generator, if you wish
#   3. Pick extra shrinkage params, if you wish
#   4. Pick love and hate ticker lists, if you wish


def m6_dump(df,file_name):
    """ Write to CSV with 'ID' in top corner """
    df.columns = ['Rank'+str(i) for i in range(1,6)] + ['Decision']
    df.reset_index().rename(columns={'index': 'ID'}).to_csv(file_name, index=False)


def m6_competition_entry(interval='d', f=None, port=None, n_dim=100, n_samples=5000, n_obs=200,
                         extra_shrink=True,
                                phi=1.1, lmbd=0.03,
                         love:[str]=None,   # List of companies you love
                         hate:[str]=None,   # List of companies you hate
                         intensity:float=1.0,
                         verbose=True):
    """
           Example of generating an M6 Entry
           pip install PyPortfolioOpt

           interval - sampling interval to use for cov estimation
           n_obs    - number of time points to use in cov estimation (max 60 if interval='m')
           n_dim    - Set at 100 for actual contest, but lower to test
           port     - A portfolio creator (see /portfolioutil )
           f        - A cov skater
           extra_shrink - If True, will perform additional shrinkage over and above the skater or portfolio method using
               phi      - (Additional) Ridge parameter, suggest (1,1.5)
               lmbd     - (Additional) Shrinkage parameter, suggest (0,0.5)
           love     - List of tickers of companies whose means will be adjusted upward slightly
           hate     - List of tickers of companies whose means will be adjusted downward slightly

    """
    if love is None:
        love = []

    if hate is None:
        hate = []

    if port is None:
        port = random_port()
        if verbose:
            print('Choosing a cov estimator from the following list ')
            pprint([p.__name__ for p in PORT])
        print('Chose '+port.__name__)


    if f is None:
        print('Choosing a cov estimator from the following list ')
        pprint(cov_skater_manifest())
        f = random_cov_skater()
        print('Choose '+f.__name__)

    print('Computing rank probabilities')
    df_prob, df_cov = m6_probabilities(f=f, interval=interval, n_dim=n_dim,
                                            n_samples=n_samples,
                                            n_obs=n_obs, verbose=verbose,
                                            love=love, hate=hate, intensity=intensity)
    cov = df_cov.values
    if extra_shrink:
        cov = affine_shrink(cov, phi=phi, lmbd=lmbd)
        cov = nearest_pos_def(cov)

    print('Computing portfolio w/ ad-hoc tilt')
    w = port(cov=cov)
    mu = affection_tilt(covdf=df_cov, love=love, hate=hate, intensity=intensity)
    w[mu>0] = w[mu>0] + 1.0/5*len(love)
    w[mu<0] = w[mu<0] - 1.0/2*len(love)

    sum_abs = sum( [abs(wi) for wi in w] )
    w_normalized = [ wi/sum_abs for wi in w]
    w_rounded = [round(wi, 5) for wi in w_normalized]

    entry = df_prob.copy()
    entry['Decision'] = w_rounded
    entry.rename(inplace=True, columns={'0': 'Rank1', '1': 'Rank2', '2': 'Rank3', '3': 'Rank4', '4': 'Rank5'})
    return entry



if __name__=='__main__':
    df = m6_competition_entry()
    m6_dump(df=df,file_name='m6_competition_entry.csv')





