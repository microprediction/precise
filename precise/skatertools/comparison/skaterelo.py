
from pprint import pprint
from precise.skatertools.comparison.skaterwinio import win_data
from precise.skatertools.comparison.eloformulas import elo_change
from collections import Counter
import random

# Creating Elo ratings from collections of wins and losses


def elo_from_win_counts(ctn):
    contestants = list(set( [ k.split('>')[0] for k in ctn.keys() ] + [ k.split('>')[1] for k in ctn.keys() ]))
    elo = Counter( dict([ (c,1500) for c in contestants ]))
    finished = False
    while not finished:
        remaining_choices = [ (b,c) for b,c in ctn.items() if c>=1 ]
        finished = not remaining_choices
        if not finished:
            b_rand = random.choice(remaining_choices)
            winner, loser = b_rand[0].split('>')
            winner_change, loser_change = elo_change(elo[winner],elo[loser],points=1.0, k=10)
            ctn[b_rand[0]] -= 1
            elo[winner] += winner_change
            elo[loser] += loser_change
    return elo


def cat_elo():
    return [ (cat, elo_from_win_counts(cat_data)) for cat, cat_data in win_data() ]



if __name__=='__main__':
   pprint(cat_elo())