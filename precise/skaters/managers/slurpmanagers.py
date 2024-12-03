from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt
from precise.inclusion.riskparityportfolioinclusion import using_riskparityportfolio

if using_pyportfolioopt and using_riskparityportfolio:
    from precise.skaters.managers.slurpmanagerfactory import slurp_vol_manager_factory

    def slurp_vol_r025_s2_p20_g000_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=2)


    def slurp_vol_r001_s2_p20_g000_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=2)


    def slurp_vol_r025_s5_p20_g000_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=5)


    def slurp_vol_r001_s5_p20_g000_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=5)


    def slurp_vol_r025_s25_p20_g000_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=25)


    def slurp_vol_r001_s25_p20_g000_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01,  e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=25)


    def slurp_vol_r025_s100_p20_g000_long_manager(y, s=100, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025, e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=100)


    def slurp_vol_r001_s100_p20_g000_long_manger(y, s=100, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0, delta=0,j=j,q=q, n_split=100)


    SLURP_GAMMA000_LONG_MANAGERS = [slurp_vol_r025_s2_p20_g000_long_manager,
                                    slurp_vol_r001_s2_p20_g000_long_manger,
                                    slurp_vol_r025_s5_p20_g000_long_manager,
                                    slurp_vol_r001_s5_p20_g000_long_manger,
                                    slurp_vol_r025_s25_p20_g000_long_manager,
                                    slurp_vol_r001_s25_p20_g000_long_manger,
                                    slurp_vol_r025_s100_p20_g000_long_manager,
                                    slurp_vol_r001_s100_p20_g000_long_manger]


    def slurp_vol_r025_s2_p20_g100_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=2)


    def slurp_vol_r001_s2_p20_g100_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=2)


    def slurp_vol_r025_s5_p20_g100_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=5)


    def slurp_vol_r001_s5_p20_g100_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=5)


    def slurp_vol_r025_s25_p20_g100_long_manager(y, s=25, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=25)


    def slurp_vol_r001_s25_p20_g100_long_manger(y, s=25, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01,  e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=25)


    def slurp_vol_r025_s100_p20_g100_long_manager(y, s=100, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025, e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=100)


    def slurp_vol_r001_s100_p20_g100_long_manger(y, s=100, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q, n_split=100)


    SLURP_GAMMA100_LONG_MANAGERS = [slurp_vol_r025_s2_p20_g100_long_manager,
                                    slurp_vol_r001_s2_p20_g100_long_manger,
                                    slurp_vol_r025_s5_p20_g100_long_manager,
                                    slurp_vol_r001_s5_p20_g100_long_manger,
                                    slurp_vol_r025_s25_p20_g100_long_manager,
                                    slurp_vol_r001_s25_p20_g100_long_manger,
                                    slurp_vol_r025_s100_p20_g100_long_manager,
                                    slurp_vol_r001_s100_p20_g100_long_manger]

    def slurp_vol_r025_s2_p20_g020_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=2)


    def slurp_vol_r001_s2_p20_g020_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=2)


    def slurp_vol_r025_s5_p20_g020_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=5)


    def slurp_vol_r001_s5_p20_g020_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=5)


    def slurp_vol_r025_s25_p20_g020_long_manager(y, s=25, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=25)


    def slurp_vol_r001_s25_p20_g020_long_manger(y, s=25, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01,  e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=25)


    def slurp_vol_r025_s100_p20_g020_long_manager(y, s=100, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.025, e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=100)


    def slurp_vol_r001_s100_p20_g020_long_manger(y, s=100, k=1, e=1,j=1,q=1.0):
        return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0.2, delta=0,j=j,q=q, n_split=100)


    SLURP_GAMMA020_LONG_MANAGERS = [slurp_vol_r025_s2_p20_g020_long_manager,
                                    slurp_vol_r001_s2_p20_g020_long_manger,
                                    slurp_vol_r025_s5_p20_g020_long_manager,
                                    slurp_vol_r001_s5_p20_g020_long_manger,
                                    slurp_vol_r025_s25_p20_g020_long_manager,
                                    slurp_vol_r001_s25_p20_g020_long_manger,
                                    slurp_vol_r025_s100_p20_g020_long_manager,
                                    slurp_vol_r001_s100_p20_g020_long_manger]


    SLURP_LONG_MANAGERS = SLURP_GAMMA000_LONG_MANAGERS + \
                          SLURP_GAMMA020_LONG_MANAGERS + \
                          SLURP_GAMMA100_LONG_MANAGERS
else:
    SLURP_LONG_MANAGERS = []

