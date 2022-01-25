from precise.skaters.covariance.empirical import EMPIRICAL_DO_COV_SKATERS, EMPIRICAL_D1_COV_SKATERS
from precise.skaters.covariance.bufferedempirical import BUFFERED_EMPIRICAL_D0_SKATERS, BUFFERED_EMPIRICAL_D1_SKATERS
from precise.skaters.covariance.bufferedsklearn import SK_BUFFERED_D0_SKATERS, SK_BUFFERED_D1_SKATERS
from precise.skaters.covariance.movingaverage import EMA_DO_COV_SKATERS, EMA_D1_COV_SKATERS

# List of fully autonomous multivariate gaussian forecasters

ALL_D0_SKATERS = BUFFERED_EMPIRICAL_D0_SKATERS + EMPIRICAL_DO_COV_SKATERS + SK_BUFFERED_D0_SKATERS + EMA_DO_COV_SKATERS
ALL_D1_SKATERS = BUFFERED_EMPIRICAL_D1_SKATERS + EMPIRICAL_D1_COV_SKATERS + SK_BUFFERED_D1_SKATERS + EMA_D1_COV_SKATERS

ALL_COV_SKATERS = ALL_D0_SKATERS + ALL_D1_SKATERS


def cov_skater_from_name(name):
    valid = [f for f in ALL_COV_SKATERS if f.__name__ == name]
    return valid[0] if len(valid)==1 else None


if __name__=='__main__':
    from pprint import pprint
    pprint(ALL_D0_SKATERS)