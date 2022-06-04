
from pprint import pprint
from precise.skatervaluation.battleutil.battleio import win_data
from precise.skatervaluation.battleutil.eloformulas import elo_change
from collections import Counter
import random
from precise.skatervaluation.battleutil.speed import TIMING
from collections import OrderedDict
import pandas as pd
from precise.whereami import ELO_CSV
# Creating Elo ratings from collections of wins and losses stored in hashed files /battleresults

GENRES = ['manager_var','manager_info','cov_likelihood']
ELO_URL = 'https://raw.githubusercontent.com/microprediction/precise/main/precise/skatervaluation/battleresults/elo.csv'

ELO_LIMIT = 50000


def get_elo(genre):
    """ Retrieve cached Elo ratings """
    url = ELO_URL.replace('elo','elo_'+genre)
    df = pd.read_csv(url)
    return df


def create_elo_csvs():
    """ Clobber the elo_***.csv files """
    print(ELO_CSV)
    for genre in GENRES:
        fn = ELO_CSV.replace('elo', 'elo_' + genre)
        print(fn)
        df = elo_df(genre=genre, category=None)
        df.to_csv(fn, index=False)


def elo_df(genre='manager_info', category='stocks'):
    """ Elo ratings in a dataframe
    :param genre:      'cov_likelihood'
    :param category:
    :return:
    """
    ratings = elo_from_win_files(genre=genre, category=category)
    elo_tuples = list()
    for r in ratings:
        cat = r[0]
        for strat, strat_stats in r[1].items():
            got_it = False
            try:
                elo_ = strat_stats[0]
                try:
                    cpu_ = round(float(strat_stats[1]),1)
                except:
                    cpu_ = -1
                got_it=True
            except:
                try:
                    elo_ = float(strat_stats)
                    cpu_ = -1
                    got_it = True
                except:
                    got_it = False
            if got_it:
                _tup = (genre,cat,strat, elo_, cpu_)
                elo_tuples.append(_tup)

    df = pd.DataFrame(columns=['genre','category','strategy','elo','cpu'], data=elo_tuples)
    return df




def elo_from_win_files(genre='cov_likelihood', category=None):
    """
    :return:  Elo ratings for all categories
    """
    # MAYBETODO: It would be easy to make this // across categories but not a high priority :)
    return [(cat, elo_from_win_counts(cat_data, timing_genre=genre)) for cat, cat_data in win_data(genre=genre, category=category)]



def elo_from_win_counts(ctn, timing_genre=None):
    """
        Elo ratings from a counter or dict of match results

        Each key is a string of the form:

              someone>someoneelse

        indicating a win of someone over someone else. Values are the number of occasions on
        which the result eventuated.

        Matches are sampled in random ordering, so the Elo ratings will be different each
        time this script is run.

        There is no temporality. When older battle results files become irrelevant they
        should simply be deleted
    """
    contestants = list(set( [ k.split('>')[0] for k in ctn.keys() ] + [ k.split('>')[1] for k in ctn.keys() ]))
    elo = Counter( dict([ (c,1500) for c in contestants ]))
    finished = False
    import time
    st = time.time()
    ct = 0
    n_limit = ELO_LIMIT
    n_count = 0
    while not finished:
        n_count += 1

        remaining_counts = [ c for b,c in ctn.items() if c>=1 ]
        remaining_battles = [ (b,c) for b,c in ctn.items() if c>=1 ]
        weights = [ c/sum(remaining_counts) for c in remaining_counts ]
        finished = (not remaining_battles) or (n_count>n_limit)
        if not finished:
            n_remaining = sum(remaining_counts)
            if n_remaining % 100 ==0:
                print('  '+str(n_remaining)+' remaining')
            cts = time.time()
            random_battle = random.choices(population=remaining_battles, weights=weights,k=1)[0]
            ct += time.time()-cts
            winner, loser = random_battle[0].split('>')
            winner_change, loser_change = elo_change(elo[winner],elo[loser],points=1.0, k=10)
            ctn[random_battle[0]] -= 1
            elo[winner] += winner_change
            elo[loser] += loser_change
    pprint({'total time':time.time()-st,'choice time':ct})
    if timing_genre is not None:
        contestant_timing = TIMING.get(timing_genre)
        if contestant_timing is not None:
            with_timing = sorted( [ (contestant,(score,contestant_timing.get(contestant))) for contestant, score in elo.items()], key= lambda x: x[1][0], reverse=True)
            elo = OrderedDict(with_timing)
    return elo


if __name__=='__main__':
    category_sub_string = 'stocks_20_days' # e.g. m6_daily_p100
    ratings = elo_df(genre='manager_var', category=category_sub_string)
    pprint(ratings)