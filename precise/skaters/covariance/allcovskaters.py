from precise.skaters.covariance.runemp import RUN_EMP_DO_COV_SKATERS, RUN_EMP_D1_COV_SKATERS
from precise.skaters.covariance.bufemp import BUF_EMP_D0_SKATERS, BUF_EMP_D1_SKATERS
from precise.skaters.covariance.bufsk import BUF_SK_D0_SKATERS, BUF_SK_D1_SKATERS
from precise.skaters.covariance.ewaemp import EMA_DO_COV_SKATERS, EXP_EMP_D1_COV_SKATERS
from precise.skaters.covariance.bufhuber import BUF_HUBER_D0_COV_SKATERS, BUF_HUBER_D1_COV_SKATERS
from precise.skaters.covariance.ewapm import EWA_PM_EMP_D0_COV_SKATERS
from precise.skaters.covariance.ewalw import EWA_LW_D0_COV_SKATERS, EWA_LW_D1_COV_SKATERS
from precise.skaters.covariance.ewalz import EWA_LZ_D0_COV_SKATERS

# List of fully autonomous multivariate gaussian forecasters

ALL_D0_SKATERS = BUF_EMP_D0_SKATERS + \
                 RUN_EMP_DO_COV_SKATERS + \
                 BUF_SK_D0_SKATERS + \
                 EMA_DO_COV_SKATERS + \
                 BUF_HUBER_D0_COV_SKATERS + \
                 EWA_PM_EMP_D0_COV_SKATERS + \
                 EWA_LW_D0_COV_SKATERS+\
                 EWA_LZ_D0_COV_SKATERS


ALL_D1_SKATERS = BUF_EMP_D1_SKATERS + \
                 RUN_EMP_D1_COV_SKATERS + \
                 BUF_SK_D1_SKATERS + \
                 EXP_EMP_D1_COV_SKATERS + \
                 BUF_HUBER_D1_COV_SKATERS + \
                 EWA_LW_D1_COV_SKATERS

ALL_COV_SKATERS = ALL_D0_SKATERS + ALL_D1_SKATERS


def cov_skater_from_name(name):
    valid = [f for f in ALL_COV_SKATERS if f.__name__ == name]
    return valid[0] if len(valid)==1 else None



if __name__=='__main__':
    # Print the manifest of scaketers and their GitHub locations
    from pprint import pprint
    from precise.whereami import url_from_skater_name
    manifest = dict([ (f.__name__, url_from_skater_name(f.__name__)) for f in ALL_COV_SKATERS ])
    pprint(manifest)