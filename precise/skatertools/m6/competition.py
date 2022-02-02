from pprint import pprint
from precise.skaters.covarianceutil.covfunctions import affine_shrink, nearest_pos_def
from precise.skaters.portfolioutil.allstaticport import PRC_PORT, random_port
from precise.skaters.covariance.allcovskaters import random_cov_skater, cov_skater_manifest
from precise.skatertools.m6.quintileprobabilities import m6_probabilities

# Demonstrates the creation of an entry in the M6 contest
#   1. Pick a cov estimator (i.e. a "cov skater")
#   2. Pick a portfolio generator
#   3. Pick extra shrinkage params if you wish


def m6_competition_entry(interval='d', f=None, port=None, n_dim=100, n_samples=5000, n_obs=200, extra_shrink=True, phi=1.1, lmbd=0.03, verbose=True):
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

    """
    if port is None:
        if verbose:
            print('Choosing a cov estimator from the following list ')
            pprint([p.__name__ for p in PRC_PORT])
        port = random_port()

    if f is None:
        print('Choosing a cov estimator from the following list ')
        pprint(cov_skater_manifest())
        f = random_cov_skater()

    print('Computing rank probabilities')
    df_prob, df_cov = m6_probabilities(f=f, interval=interval, n_dim=n_dim, n_samples=n_samples, n_obs=n_obs)
    cov = df_cov.values
    if extra_shrink:
        cov = affine_shrink(cov, phi=phi, lmbd=lmbd)
        cov = nearest_pos_def(cov)
    print('Computing portfolio')
    w = port(cov=cov)

    # Normalize portfolio sum |w|=1
    sum_abs = sum( [abs(wi) for wi in w] )
    w_normalized = [ wi/sum_abs for wi in w]
    w_rounded = [round(wi, 5) for wi in w_normalized]

    entry = df_prob.copy()
    entry['Decision'] = w_rounded
    entry.rename(inplace=True, columns={'0': 'Rank1', '1': 'Rank2', '2': 'Rank3', '3': 'Rank4', '4': 'Rank5'})
    return entry



if __name__=='__main__':
    from precise.whereami import TOP
    df = m6_competition_entry()
    df.to_csv('m6_competition_entry.csv')





