
from pprint import pprint
from precise.skatervaluation.battleutil.battleio import win_data
from precise.skatervaluation.battleutil.eloformulas import elo_change
from collections import Counter
import random
from precise.skatervaluation.battleutil.speed import TIMING
from collections import OrderedDict
# Creating Elo ratings from collections of wins and losses stored in hashed files /battleresults



def elo_from_win_files(genre='cov_likelihood'):
    """
    :return:  Elo ratings for all categories
    """
    # MAYBETODO: It would be easy to make this // across categories but not a high priority :)
    the_lot = [(cat, elo_from_win_counts(cat_data, timing_genre=genre)) for cat, cat_data in win_data(genre=genre)]
    return the_lot


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
    while not finished:
        remaining_counts = [ c for b,c in ctn.items() if c>=1 ]
        remaining_battles = [ (b,c) for b,c in ctn.items() if c>=1 ]
        weights = [ c/sum(remaining_counts) for c in remaining_counts ]
        finished = not remaining_battles
        if not finished:
            random_battle = random.choices(population=remaining_battles, weights=weights,k=1)[0]
            winner, loser = random_battle[0].split('>')
            winner_change, loser_change = elo_change(elo[winner],elo[loser],points=1.0, k=10)
            ctn[random_battle[0]] -= 1
            elo[winner] += winner_change
            elo[loser] += loser_change
    if timing_genre is not None:
        contestant_timing = TIMING.get(timing_genre)
        if contestant_timing is not None:
            with_timing = sorted( [ (contestant,(score,contestant_timing.get(contestant))) for contestant, score in elo.items()], key= lambda x: x[1][0], reverse=True)
            elo = OrderedDict(with_timing)
    return elo



if __name__=='__main__':
    category_sub_string = 'stocks' # e.g. m6_daily_p100
    ratings = elo_from_win_files(genre='manager_var')
    pprint([ r for r in ratings if category_sub_string in r[0]])