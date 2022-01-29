from runthis import parse_kwargs
from precise.skatervaluation.battleutil.arrangingbattles import skater_battle
import os

# Infers params from file name and runs a battle

if __name__=='__main__':
    params = parse_kwargs(__file__.split(os.path.sep)[-1])
    skater_battle(params=params)