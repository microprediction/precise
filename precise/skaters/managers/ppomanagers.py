from precise.skaters.managers.ppomanagerfactory import ppo_ewa_long_manager_factory, ppo_pm_long_manager_factory

# PyPortfolioOpt managers that use partial moments cov estimation
# ['max_sharpe','min_volatility','max_quadratic_utility']


def ppo_pm_t0_d0_r025_n50_vol_long_manager(y, s, k=1):
    assert k == 1
    return ppo_pm_long_manager_factory(y=y, s=s, method='min_volatility', target=0, r=0.025, n_emp=50)


def ppo_ewa_d0_r025_n50_vol_long_manager(y, s, k=1):
    assert k == 1
    return ppo_ewa_long_manager_factory(y=y, s=s, method='min_volatility', r=0.025, n_emp=50)


def ppo_pm_t0_d0_r025_n50_quad_long_manager(y, s, k=1):
    assert k == 1
    return ppo_pm_long_manager_factory(y=y, s=s, method='max_quadratic_utility', target=0, r=0.025, n_emp=50)


def ppo_ewa_d0_r025_n50_quad_long_manager(y, s, k=1):
    assert k == 1
    return ppo_ewa_long_manager_factory(y=y, s=s, method='max_quadratic_utility', r=0.025, n_emp=50)


def ppo_pm_t0_d0_r025_n50_sharpe_long_manager(y, s, k=1):
    assert k == 1
    return ppo_pm_long_manager_factory(y=y, s=s, method='max_sharpe', target=0, r=0.025, n_emp=50)


def ppo_ewa_d0_r025_n50_sharpe_long_manager(y, s, k=1):
    assert k == 1
    return ppo_ewa_long_manager_factory(y=y, s=s, method='max_sharpe', r=0.025, n_emp=50)


PPO_LONG_MANGERS = [ppo_pm_t0_d0_r025_n50_vol_long_manager,
                    ppo_ewa_d0_r025_n50_vol_long_manager,
                    ppo_pm_t0_d0_r025_n50_quad_long_manager,
                    ppo_ewa_d0_r025_n50_quad_long_manager,
                    ppo_ewa_d0_r025_n50_quad_long_manager,
                    ppo_pm_t0_d0_r025_n50_sharpe_long_manager,
                    ppo_ewa_d0_r025_n50_sharpe_long_manager]
