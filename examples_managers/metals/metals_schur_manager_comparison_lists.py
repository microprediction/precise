from precise.skatertools.data.preciousmetalsreturns import precious_metals_returns
from precise.skaters.managers.schurmanagers import SCHUR_MANAGERS
from precise.skatervaluation.managercomparisonutil.managerstats import manager_stats_leaderboard
from precise.skaters.managers.equalmanagers import equal_long_manager

# Similar example but uses lists

mrgs = [equal_long_manager] + SCHUR_MANAGERS

if __name__=='__main__':
    xs = precious_metals_returns()[-1000:]
    j = 20   # How often to rebalance
    q = 1.0 # How far to move towards target when rebalancing
    lb = manager_stats_leaderboard(mgrs=mrgs, xs=xs, verbose=True, field='info', j=j, q=q)





