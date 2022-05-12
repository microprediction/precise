from runthis import parse_kwargs
from precise.skatervaluation.battleutil.arrangingbattles import manager_var_battle
import os


# Hey thanks for running this, it will generate more Elo rating data
# The results will be put in a new file in precise/battleresults/manager_var/
# You can PR the new file if you are so kind.

SCRIPT = 'stocks?topic=stocks&n_dim=int:500&n_obs=int:225&n_burn=int:200&k=int:5.py'

if __name__=='__main__':
    params = parse_kwargs(SCRIPT.split(os.path.sep)[-1])
    manager_var_battle(params=params)


