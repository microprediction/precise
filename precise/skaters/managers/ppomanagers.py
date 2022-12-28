from precise.skaters.managers.ppomanagerfactory import ppo_ewa_long_manager_factory, ppo_pm_long_manager_factory, ppo_long_manager_factory
from precise.skaters.covariance.bufsk import buf_sk_glcv_pcov_d0_n100, buf_sk_glcv_pcov_d0_n100_t0, buf_sk_lw_pcov_d0_n100, buf_sk_mcd_pcov_d0_n100
from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt


if using_pyportfolioopt:
    # PyPortfolioOpt managers

    def ppo_pm_t0_d0_r025_n50_vol_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        assert k == 1
        return ppo_pm_long_manager_factory(y=y, s=s, method='min_volatility', target=0, e=e, j=j,r=0.025,n_emp=50,q=q)


    def ppo_ewa_d0_r025_n50_vol_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        assert k == 1
        return ppo_ewa_long_manager_factory(y=y, s=s, method='min_volatility', e=e, j=j,r=0.025,n_emp=50,q=q)


    def ppo_pm_t0_d0_r025_n50_quad_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        assert k == 1
        return ppo_pm_long_manager_factory(y=y, s=s, method='max_quadratic_utility', target=0, e=e, j=j,r=0.025,n_emp=50,q=q)


    def ppo_ewa_d0_r025_n50_quad_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        assert k == 1
        return ppo_ewa_long_manager_factory(y=y, s=s, method='max_quadratic_utility', e=e, j=j,r=0.025,n_emp=50,q=q)


    def ppo_pm_t0_d0_r025_n50_sharpe_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        assert k == 1
        return ppo_pm_long_manager_factory(y=y, s=s, method='max_sharpe', target=0, e=e, j=j,r=0.025,n_emp=50,q=q)


    def ppo_ewa_d0_r025_n50_sharpe_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        assert k == 1
        return ppo_ewa_long_manager_factory(y=y, s=s, method='max_sharpe', e=e, j=j,r=0.025,n_emp=50,q=q)


    # Sklearn with min vol

    def ppo_sk_lw_pcov_d1_n100_vol_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_lw_pcov_d0_n100, e=e, j=j,method='min_volatility',q=q)


    def ppo_sk_glcv_pcov_d0_n100_vol_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100, e=e, j=j,method='min_volatility',q=q)


    def ppo_sk_glcv_pcov_d0_n100_t0_vol_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100_t0, e=e, j=j,method='min_volatility',q=q)


    def ppo_sk_mcd_pcov_d0_n100_vol_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_mcd_pcov_d0_n100, e=e, j=j,method='min_volatility',q=q)


    # Sklearn with quadratic util

    def ppo_sk_lw_pcov_d0_n100_quad_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_lw_pcov_d0_n100, e=e, j=j,method='max_quadratic_utility',q=q)


    def ppo_sk_glcv_pcov_d0_n100_quad_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100, e=e, j=j,method='max_quadratic_utility',q=q)


    def ppo_sk_glcv_pcov_d0_n100_t0_quad_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100_t0, e=e, j=j,method='max_quadratic_utility',q=q)


    def ppo_sk_mcd_pcov_d0_n100_quad_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_mcd_pcov_d0_n100, e=e, j=j,method='max_quadratic_utility',q=q)



    # Sklearn with max sharpe

    def ppo_sk_lw_pcov_d0_n100_sharpe_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_lw_pcov_d0_n100, method='max_sharpe',j=j,q=q)


    def ppo_sk_glcv_pcov_d0_n100_sharpe_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100, method='max_sharpe',j=j,q=q)


    def ppo_sk_glcv_pcov_d0_n100_t0_sharpe_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_glcv_pcov_d0_n100_t0, method='max_sharpe',j=j,q=q)


    def ppo_sk_mcd_pcov_d0_n100_sharpe_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return ppo_long_manager_factory(y=y,s=s,f=buf_sk_mcd_pcov_d0_n100, method='max_sharpe',j=j,q=q)


    PPO_LONG_MANAGERS = [ppo_pm_t0_d0_r025_n50_vol_long_manager,
                         ppo_ewa_d0_r025_n50_vol_long_manager,
                         ppo_pm_t0_d0_r025_n50_quad_long_manager,
                         ppo_ewa_d0_r025_n50_quad_long_manager,
                         ppo_ewa_d0_r025_n50_quad_long_manager,
                         ppo_pm_t0_d0_r025_n50_sharpe_long_manager,
                         ppo_ewa_d0_r025_n50_sharpe_long_manager,
                         ppo_sk_lw_pcov_d1_n100_vol_long_manager,
                         ppo_sk_glcv_pcov_d0_n100_vol_long_manager,
                         ppo_sk_glcv_pcov_d0_n100_t0_vol_long_manager,
                         ppo_sk_mcd_pcov_d0_n100_vol_long_manager,
                         ppo_sk_lw_pcov_d0_n100_quad_long_manager,
                         ppo_sk_glcv_pcov_d0_n100_quad_long_manager,
                         ppo_sk_glcv_pcov_d0_n100_t0_quad_long_manager,
                         ppo_sk_mcd_pcov_d0_n100_quad_long_manager,
                         ppo_sk_lw_pcov_d0_n100_sharpe_long_manager,
                         ppo_sk_glcv_pcov_d0_n100_sharpe_long_manager,
                         ppo_sk_glcv_pcov_d0_n100_t0_sharpe_long_manager,
                         ppo_sk_mcd_pcov_d0_n100_sharpe_long_manager]
else:
    PPO_LONG_MANAGERS = []


if __name__=='__main__':
    mgr = ppo_pm_t0_d0_r025_n50_sharpe_long_manager
    from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run
    manager_test_run(mgr=mgr,n_dim=5, n_obs=50)
