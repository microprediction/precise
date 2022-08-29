import runthis
from runthis import parse_kwargs
import os
from precise.skaters.managerutil.managerstats import manager_info, manager_var

# Infers params from file name and runs a battle
from precise.skaters.managers.schurmanagers import SCHUR_PM_S5_LONG_MANAGERS
from precise.skaters.managers.hrpmanagers import HRP_LONG_MANAGERS
from precise.skatervaluation.battleutil.arrangingbattles import generic_battle

if __name__=='__main__':
    params = parse_kwargs(__file__.split(os.path.sep)[-1])
    generic_battle(contestants=SCHUR_PM_S5_LONG_MANAGERS+HRP_LONG_MANAGERS, evaluator=manager_var, params=params, atol=1e-8)
