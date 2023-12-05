from precise.inclusion.riskparityportfolioinclusion import using_riskparityportfolio
if using_riskparityportfolio:
    import random
    from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run, manager_debug_run
    from precise.skaters.managers.rpmanagers import rp_ewa_r01_p40_l21_long_manager as troublesome_mgr



    def test_random_manager():
        from precise.skaters.managers.rpmanagers import RP_STOCHASTIC_LONG_MANAGERS
        HULL = [s for s in RP_STOCHASTIC_LONG_MANAGERS if 'l21' in s.__name__]
        mgr = random.choice(HULL)
        j = random.choice([1, 5, 20])
        q = random.choice([1.0, 0.1])
        manager_test_run(mgr=mgr, j=j, q=q)

