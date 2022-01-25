from precise.skaters.covariance.movingaveragepre import ema_pcov_r
from precise.skaters.covarianceutil.conventions import Y_DATA_TYPE
from precise.skaters.covarianceutil.differencing import d1_factory


def ema_pcov_d0_r01(y,s,k=1):
    return ema_pcov_r(y=y,s=s,k=k,r=0.01)


def ema_pcov_d0_r02(y,s,k=1):
    return ema_pcov_r(y=y,s=s,k=k,r=0.02)


def ema_pcov_d0_r05(y,s,k=1):
    return ema_pcov_r(y=y,s=s,k=k,r=0.05)


def ema_pcov_d0_r10(y,s,k=1):
    return ema_pcov_r(y=y,s=s,k=k,r=0.10)


EMA_DO_COV_SKATERS = [ ema_pcov_d0_r01, ema_pcov_d0_r02, ema_pcov_d0_r05, ema_pcov_d0_r10  ]


def ema_pcov_d1_r01( y:Y_DATA_TYPE, s:dict, k=1):
    """
        For when changes are iid gaussian
    """
    return d1_factory( f = ema_pcov_d0_r01, y=y, s=s, k=k )


def ema_pcov_d1_r02( y:Y_DATA_TYPE, s:dict, k=1):
    return d1_factory( f = ema_pcov_d0_r02, y=y, s=s, k=k )


def ema_pcov_d1_r05( y:Y_DATA_TYPE, s:dict, k=1):
    return d1_factory( f = ema_pcov_d0_r05, y=y, s=s, k=k )


def ema_pcov_d1_r10( y:Y_DATA_TYPE, s:dict, k=1):
    return d1_factory( f = ema_pcov_d0_r10, y=y, s=s, k=k )


EMA_D1_COV_SKATERS = [ ema_pcov_d1_r01, ema_pcov_d1_r02, ema_pcov_d1_r05, ema_pcov_d1_r10  ]

