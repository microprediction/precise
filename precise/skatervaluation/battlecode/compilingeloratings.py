
from pprint import pprint
from precise.skatervaluation.battlecode.battleio import win_data
from precise.skatervaluation.battlecode.eloformulas import elo_change
from collections import Counter
import random

# Creating Elo ratings from collections of wins and losses stored in hashed files /skaterwindata


def elo_from_win_counts(ctn):
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
    return elo


def cat_elo():
    return [ (cat, elo_from_win_counts(cat_data)) for cat, cat_data in win_data() ]



if __name__=='__main__':
   pprint(cat_elo())