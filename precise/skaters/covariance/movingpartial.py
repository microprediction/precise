from precise.skaters.covariance.movingpartialpre import partial_ema_scov_factory


def partial_ema_scov_r01(s,y,k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.01)


def partial_ema_scov_r02(s,y,k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.02)


def partial_ema_scov_r05(s,y,k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.05)


def partial_ema_scov_r01_t0(s,y,k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.01, target=0)


def partial_ema_scov_r02_t0(s,y,k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.02, target=0)


def partial_ema_scov_r05_t0(s,y,k=1):
    return partial_ema_scov_factory(s=s,y=y,k=k,r=0.05, target=0)


PARTIAL_EMA_D0_COV_SKATERS = [partial_ema_scov_r01, partial_ema_scov_r02, partial_ema_scov_r05,
                              partial_ema_scov_r01_t0, partial_ema_scov_r02_t0, partial_ema_scov_r05_t0 ]