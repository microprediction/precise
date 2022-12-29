from precise.skatertools.data.preciousmetalsreturns import precious_metals_returns
from precise.skaters.managers.schurmanagers import SCHUR_MANAGERS
from precise.skatervaluation.managercomparisonutil.managerstats import manager_stats_leaderboard
from precise.skaters.managers.equalmanagers import equal_long_manager

# Similar example but uses lists

filtered_managers = [ mgr for mgr in SCHUR_MANAGERS if ('diag' in mgr.__name__) and 'ewa' in mgr.__name__]
mrgs = [equal_long_manager] + filtered_managers

if __name__=='__main__':
    xs = precious_metals_returns()[4000:5000]
    j = 20   # How often to rebalance
    q = 0.25 # How far to move towards target when rebalancing
    lb = manager_stats_leaderboard(mgrs=mrgs, xs=xs, verbose=True, field='info', j=j, q=q)





