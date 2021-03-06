from runthis import parse_kwargs
from precise.skatervaluation.battleutil.arrangingbattles import manager_var_battle, manager_info_battle
import os


# Hey thanks for running this, it will generate more Elo rating data
# The results will be put in a new file in precise/battleresults/manager_var/
# You can PR the new file if you are so kind.

SCRIPT = 'stocks?topic=stocks&n_dim=int:100&n_obs=int:125&n_burn=int:100&k=int:20.py'
SCRIPT = 'stocks?topic=stocks&n_dim=int:500&n_obs=int:200&n_burn=int:90&k=int:1.py'


if __name__=='__main__':
    params = parse_kwargs(SCRIPT.split(os.path.sep)[-1])
    manager_info_battle(params=params)


