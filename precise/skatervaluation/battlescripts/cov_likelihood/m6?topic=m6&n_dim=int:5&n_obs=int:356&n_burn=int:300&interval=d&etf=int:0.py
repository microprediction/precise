from runthis import parse_kwargs
from precise.skatervaluation.battleutil.arrangingbattles import cov_likelihood_battle
import os

# Infers params from file name and runs a battle

if __name__=='__main__':
    params = parse_kwargs(__file__.split(os.path.sep)[-1])
    cov_likelihood_battle(params=params)