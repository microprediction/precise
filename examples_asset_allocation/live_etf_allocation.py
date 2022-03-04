from precise.skatertools.data.equitylive import live_veteran_etf_data
from precise.skatertools.data.etflists import VETERAN_NON_BOND_ETFS
from itertools import zip_longest
from pprint import pprint

# Use a "manager" to allocate to 40 ETFs
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
    portfolios = dict()

    # See what final portfolio the managers arrive at
    for mgr in managers:
        s = {}
        for y in xs[:-1]:
            w, s = mgr(y=y,s=s,e=-1)
        w, s = mgr(s=s, y=xs[-1],e=1)
        w = [round(wi,ndigits=4) for wi in w]
        # Display in order of allocation
        portfolio = sorted( list(zip_longest(w,VETERAN_NON_BOND_ETFS)), reverse=True )
        brief_portfolio = [ (w,name) for w,name in portfolio if abs(w)>0 ]
        print('Manager '+mgr.__name__+' suggests ')
        pprint(brief_portfolio)
        portfolios[mgr.__name__] = brief_portfolio

    import json
    with open('etf_allocation.json', 'wt') as fh:
        json.dump(portfolios,fh)



