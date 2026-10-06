from precise.skatervaluation.managercomparisonutil.managerstats import manager_info

# Runs a battle with the parameters given below
from precise.skaters.managers.schurmanagers import SCHUR_PM_S5_LONG_MANAGERS
from precise.skaters.managers.hrpmanagers import HRP_LONG_MANAGERS
from precise.skatervaluation.battleutil.arrangingbattles import generic_battle

if __name__=='__main__':
    # Parameters were once parsed from this file's name (a URL query string), which Windows
    # cannot check out; they are now written out explicitly.
    params = {'topic': 'stocks', 'n_dim': 41, 'n_obs': 125, 'n_burn': 100, 'k': 3}
    generic_battle(contestants=SCHUR_PM_S5_LONG_MANAGERS+HRP_LONG_MANAGERS, evaluator=manager_info, params=params, atol=1e-8)
