from precise.skaters.covariance.avgfactory import avg_factory
from precise.skaters.covariance.weakewa import WEAK_EWA_DO_COV_SKATERS
from precise.skaters.covariance.ewalw import EWA_LW_D0_COV_SKATERS
from precise.skaters.covariance.weakpm import WEAK_PM_DO_COV_SKATERS

FAST_AND_PRETTY_GOOD = WEAK_EWA_DO_COV_SKATERS + EWA_LW_D0_COV_SKATERS + WEAK_PM_DO_COV_SKATERS


def avg_top_weakewa_ewalw_weakpm(y, s:dict, k=1, e=1):
    assert k==1
    return avg_factory(y, fs=FAST_AND_PRETTY_GOOD, s=s, k=k, e=e)


AVG_TOP_COV_D0_SKATERS = [ avg_top_weakewa_ewalw_weakpm ]