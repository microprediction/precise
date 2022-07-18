from precise.skaters.managers.molybogamanagerfactory import molyboga_manager_factory


# A Modified Hierarchical Risk Parity Framework for Portfolio Management
# Inspired by Marat Molyboga
# https://jfds.pm-research.com/content/early/2020/07/03/jfds.2020.1.038


def molyboga_r025_s5_gamma000_long_manager(y, s=5, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=0, delta=0,j=j,q=q)


def molyboga_r001_s5_gamma000_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=0, delta=0,j=j,q=q)


def molyboga_r025_s25_gamma000_long_manager(y, s=25, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=0, delta=0,j=j,q=q)


def molyboga_r001_s25_gamma000_long_manger(y, s=25, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.01,  e=e, gamma=0, delta=0,j=j,q=q)


def molyboga_r025_s100_gamma000_long_manager(y, s=100, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.025, e=e, gamma=0, delta=0,j=j,q=q)


def molyboga_r001_s100_gamma000_long_manger(y, s=100, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=0, delta=0,j=j,q=q)


MOLYBOGA_GAMMA000_LONG_MANAGERS = [molyboga_r025_s5_gamma000_long_manager,
                                   molyboga_r001_s5_gamma000_long_manger,
                                   molyboga_r025_s25_gamma000_long_manager,
                                   molyboga_r001_s25_gamma000_long_manger,
                                   molyboga_r025_s100_gamma000_long_manager,
                                   molyboga_r001_s100_gamma000_long_manger]



def molyboga_r025_s5_gamma100_long_manager(y, s=5, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q)


def molyboga_r001_s5_gamma100_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q)


def molyboga_r025_s25_gamma100_long_manager(y, s=25, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.025,  e=e, gamma=1.0, delta=0,j=j,q=q)


def molyboga_r001_s25_gamma100_long_manger(y, s=25, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.01,  e=e, gamma=1.0, delta=0,j=j,q=q)


def molyboga_r025_s100_gamma100_long_manager(y, s=100, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.025, e=e, gamma=1.0, delta=0,j=j,q=q)


def molyboga_r001_s100_gamma100_long_manger(y, s=100, k=1, e=1,j=1,q=1.0):
    return molyboga_manager_factory(y=y, s=s, r=0.01, e=e, gamma=1.0, delta=0,j=j,q=q)


MOLYBOGA_GAMMA100_LONG_MANAGERS = [molyboga_r025_s5_gamma100_long_manager,
                                   molyboga_r001_s5_gamma100_long_manger,
                                   molyboga_r025_s25_gamma100_long_manager,
                                   molyboga_r001_s25_gamma100_long_manger,
                                   molyboga_r025_s100_gamma100_long_manager,
                                   molyboga_r001_s100_gamma100_long_manger]


MOLYBOGA_LONG_MANGERS = MOLYBOGA_GAMMA000_LONG_MANAGERS + MOLYBOGA_GAMMA100_LONG_MANAGERS
