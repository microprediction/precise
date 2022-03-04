from precise.skatertools.data.equitylive import live_veteran_etf_data
from pprint import pprint
from precise.skaters.managerutil.managerstats import manager_stats
import json
import numpy as np

# Look at manager performance for about 40 ETFs
# (Pulls data slowly so be patient!)
# Not investment advice, just an show_em


if __name__=='__main__':
    # Select some managers
    from precise.skaters.managers.weakmanagers import weak_sk_lw_pcov_d0_n100_long_manager, weak_pm_t0_d0_r050_n50_long_manager
    from precise.skaters.managers.schurmanagers import schur_weak_vol_ewa_r050_n25_s5_g000_long_manager
    from precise.skaters.managers.hrpmanagers import hrp_weak_weak_pm_t0_d0_r025_n50_s5_long_manager
    from precise.skaters.managers.ppomanagers import ppo_ewa_d0_r025_n50_vol_long_manager, ppo_sk_glcv_pcov_d0_n100_t0_vol_long_manager
    managers = [weak_sk_lw_pcov_d0_n100_long_manager, weak_pm_t0_d0_r050_n50_long_manager, schur_weak_vol_ewa_r050_n25_s5_g000_long_manager,
                hrp_weak_weak_pm_t0_d0_r025_n50_s5_long_manager, ppo_ewa_d0_r025_n50_vol_long_manager, ppo_sk_glcv_pcov_d0_n100_t0_vol_long_manager]

    # Get some ETF returns from those that have been around for a while
    print('Be patient ...')
    df = live_veteran_etf_data(k=3)
    xs = df.values
    n_obs, n_dim = np.shape(xs)

    # Evaluate them based on daily performance
    manager_statistics = dict()
    for mgr in managers:
        print('Evaluating '+str(mgr.__name__))
        manager_statistics[mgr.__name__] = manager_stats(mgr=mgr, xs=xs, n_burn=int(n_obs/2))
        pprint( manager_statistics[mgr.__name__] )
    pprint(manager_statistics)


    with open('etf_manager_stats.json', 'wt') as fh:
        json.dump(manager_statistics,fh)



