from precise.inclusion.pyportfoliooptinclusion import using_pyportfolioopt

if using_pyportfolioopt:

    from precise.skaters.managers.molybogamanagerfactory import molyboga_manager_factory


    # A Modified Hierarchical Risk Parity Framework for Portfolio Management
    # Inspired by Marat Molyboga
    # https://jfds.pm-research.com/content/early/2020/07/03/jfds.2020.1.038


    def molyboga_r025_s2_gamma000_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=0, delta=0,j=j,q=q, n_split=2)


    def molyboga_r001_s2_gamma000_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=0, delta=0,j=j,q=q, n_split=2)


    def molyboga_r025_s5_gamma000_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=0, delta=0,j=j,q=q, n_split=5)


    def molyboga_r001_s5_gamma000_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=0, delta=0,j=j,q=q, n_split=5)


    def molyboga_r025_s25_gamma000_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=0, delta=0,j=j,q=q, n_split=25)


    def molyboga_r001_s25_gamma000_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01,  e=e, gamma=0, delta=0,j=j,q=q, n_split=25)


    def molyboga_r025_s100_gamma000_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025, e=e, gamma=0, delta=0,j=j,q=q,n_split=100)


    def molyboga_r001_s100_gamma000_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=0, delta=0,j=j,q=q, n_split=100)


    MOLYBOGA_GAMMA000_LONG_MANAGERS = [molyboga_r025_s2_gamma000_long_manager,
                                       molyboga_r001_s2_gamma000_long_manger,
                                       molyboga_r025_s5_gamma000_long_manager,
                                       molyboga_r001_s5_gamma000_long_manger,
                                       molyboga_r025_s25_gamma000_long_manager,
                                       molyboga_r001_s25_gamma000_long_manger,
                                       molyboga_r025_s100_gamma000_long_manager,
                                       molyboga_r001_s100_gamma000_long_manger]


    def molyboga_r025_s2_gamma100_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=2)


    def molyboga_r001_s2_gamma100_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=2)


    def molyboga_r025_s5_gamma100_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=5)


    def molyboga_r001_s5_gamma100_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=5)


    def molyboga_r025_s25_gamma100_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=25)

    def molyboga_r001_s25_gamma100_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=25)


    def molyboga_r025_s100_gamma100_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=100)


    def molyboga_r001_s100_gamma100_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=100)


    MOLYBOGA_GAMMA100_LONG_MANAGERS = [molyboga_r025_s2_gamma100_long_manager,
                                       molyboga_r001_s2_gamma100_long_manger,
                                       molyboga_r025_s5_gamma100_long_manager,
                                       molyboga_r001_s5_gamma100_long_manger,
                                       molyboga_r025_s25_gamma100_long_manager,
                                       molyboga_r001_s25_gamma100_long_manger,
                                       molyboga_r025_s100_gamma100_long_manager,
                                       molyboga_r001_s100_gamma100_long_manger]


    def molyboga_r025_s2_gamma020_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=2)


    def molyboga_r001_s2_gamma020_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=2)



    def molyboga_r025_s5_gamma020_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=5)


    def molyboga_r001_s5_gamma020_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=5)


    def molyboga_r025_s25_gamma020_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=25)


    def molyboga_r001_s25_gamma020_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01,  e=e, gamma=1.0, delta=0,j=j,q=q, n_split=25)


    def molyboga_r025_s100_gamma020_long_manager(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.025, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=100)


    def molyboga_r001_s100_gamma020_long_manger(y, s, k=1, e=1,j=1,q=1.0):
        return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q, n_split=100)


    MOLYBOGA_GAMMA020_LONG_MANAGERS = [molyboga_r025_s2_gamma020_long_manager,
                                       molyboga_r001_s2_gamma020_long_manger,
                                       molyboga_r025_s5_gamma020_long_manager,
                                       molyboga_r001_s5_gamma020_long_manger,
                                       molyboga_r025_s25_gamma020_long_manager,
                                       molyboga_r001_s25_gamma020_long_manger,
                                       molyboga_r025_s100_gamma020_long_manager,
                                       molyboga_r001_s100_gamma020_long_manger]


    MOLYBOGA_LONG_MANGERS = MOLYBOGA_GAMMA000_LONG_MANAGERS +\
                            MOLYBOGA_GAMMA020_LONG_MANAGERS +\
                            MOLYBOGA_GAMMA100_LONG_MANAGERS
else:
    MOLYBOGA_LONG_MANGERS =[]
