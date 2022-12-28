from precise.skatertools.data.preciousmetalsreturns import precious_metals_returns
from precise.skaters.managers.schurmanagers import schur_diag_weak_pm_t0_r050_n25_s5_g100_long_manager,\
    schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager
from precise.skaters.managers.schurmanagers import schur_weak_diag_pm_t0_r050_n25_s5_g100_long_manager, \
    schur_weak_diag_pm_t0_r050_n25_s5_g010_l7_long_manager, schur_weak_diag_pm_t0_r050_n25_s5_g050_long_manager
from precise.skatervaluation.managercomparisonutil.managerstats import manager_stats_leaderboard
from precise.skaters.managers.equalmanagers import equal_long_manager
from pprint import pprint

mrgs = [equal_long_manager,
        schur_diag_weak_pm_t0_r050_n25_s5_g100_long_manager,
        schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager,
        schur_diag_weak_pm_t0_r050_n25_s5_g050_long_manager,
        schur_weak_diag_pm_t0_r050_n25_s5_g100_long_manager,
        schur_weak_diag_pm_t0_r050_n25_s5_g010_l7_long_manager,
        schur_weak_diag_pm_t0_r050_n25_s5_g050_long_manager]


if __name__=='__main__':
    xs = precious_metals_returns()[-1000:]
    j = 1   # How often to rebalance
    q = 1.0 # How far to move towards target when rebalancing
    lb = manager_stats_leaderboard(mgrs=mrgs, xs=xs, verbose=True, field='info', j=j, q=q)
    pprint(lb)





