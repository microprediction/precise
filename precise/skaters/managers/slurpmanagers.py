from precise.skaters.managers.slurpmanagerfactory import slurp_vol_manager_factory, slurp_weak_manager_factory


def slurp_vol_r025_s5_phi20_gamma000_long_manager(y, s=5, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0, delta=0,j=j,q=q)


def slurp_vol_r001_s5_phi20_gamma000_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0, delta=0,j=j,q=q)


def slurp_vol_r025_s25_phi20_gamma000_long_manager(y, s=25, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=0, delta=0,j=j,q=q)


def slurp_vol_r001_s25_phi20_gamma000_long_manger(y, s=25, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.01,  e=e, phi=0.20, gamma=0, delta=0,j=j,q=q)


def slurp_vol_r025_s100_phi20_gamma000_long_manager(y, s=100, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.025, e=e, phi=0.20, gamma=0, delta=0,j=j,q=q)


def slurp_vol_r001_s100_phi20_gamma000_long_manger(y, s=100, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=0, delta=0,j=j,q=q)


SLURP_GAMMA000_LONG_MANAGERS = [slurp_vol_r025_s5_phi20_gamma000_long_manager,
                                slurp_vol_r001_s5_phi20_gamma000_long_manger,
                                slurp_vol_r025_s25_phi20_gamma000_long_manager,
                                slurp_vol_r001_s25_phi20_gamma000_long_manger,
                                slurp_vol_r025_s100_phi20_gamma000_long_manager,
                                slurp_vol_r001_s100_phi20_gamma000_long_manger]


def slurp_vol_r025_s5_phi20_gamma100_long_manager(y, s=5, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q)


def slurp_vol_r001_s5_phi20_gamma100_long_manger(y, s=5, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q)


def slurp_vol_r025_s25_phi20_gamma100_long_manager(y, s=25, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.025,  e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q)


def slurp_vol_r001_s25_phi20_gamma100_long_manger(y, s=25, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.01,  e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q)


def slurp_vol_r025_s100_phi20_gamma100_long_manager(y, s=100, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.025, e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q)


def slurp_vol_r001_s100_phi20_gamma100_long_manger(y, s=100, k=1, e=1,j=1,q=1.0):
    return slurp_vol_manager_factory(y=y, s=s, r=0.01, e=e, phi=0.20, gamma=1.0, delta=0,j=j,q=q)


SLURP_GAMMA100_LONG_MANAGERS = [slurp_vol_r025_s5_phi20_gamma100_long_manager,
                                slurp_vol_r001_s5_phi20_gamma100_long_manger,
                                slurp_vol_r025_s25_phi20_gamma100_long_manager,
                                slurp_vol_r001_s25_phi20_gamma100_long_manger,
                                slurp_vol_r025_s100_phi20_gamma100_long_manager,
                                slurp_vol_r001_s100_phi20_gamma100_long_manger]

SLURP_LONG_MANAGERS = SLURP_GAMMA000_LONG_MANAGERS + SLURP_GAMMA100_LONG_MANAGERS
