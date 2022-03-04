from precise.skaters.covariance.runemp import RUN_EMP_DO_COV_SKATERS, RUN_EMP_D1_COV_SKATERS
from precise.skaters.covariance.bufemp import BUF_EMP_D0_SKATERS, BUF_EMP_D1_SKATERS
from precise.skaters.covariance.bufsk import BUF_SK_D0_SKATERS, BUF_SK_D1_SKATERS
from precise.skaters.covariance.ewaemp import EMA_DO_COV_SKATERS, EXP_EMP_D1_COV_SKATERS
from precise.skaters.covariance.bufhuber import BUF_HUBER_D0_COV_SKATERS, BUF_HUBER_D1_COV_SKATERS
from precise.skaters.covariance.ewapm import EWA_PM_EMP_D0_COV_SKATERS
from precise.skaters.covariance.ewalw import EWA_LW_D0_COV_SKATERS, EWA_LW_D1_COV_SKATERS
from precise.skaters.covariance.ewalz import EWA_LZ_D0_COV_SKATERS
from precise.skaters.covariance.weakewa import WEAK_EWA_DO_COV_SKATERS
from precise.skaters.covariance.weakpm import WEAK_PM_DO_COV_SKATERS
from precise.skaters.covariance.weaklz import WEAK_LZ_DO_COV_SKATERS
from precise.skaters.covariance.weaksk import WEAK_SK_DO_COV_SKATERS

import random
from precise.whereami import COV_SKATER_MANIFEST
from tomark import Tomark

# List of fully autonomous multivariate gaussian forecasters
# Run this file to print a list of skaters and their code URLs

ALL_D0_SKATERS = BUF_EMP_D0_SKATERS + \
                 RUN_EMP_DO_COV_SKATERS + \
                 BUF_SK_D0_SKATERS + \
                 EMA_DO_COV_SKATERS + \
                 BUF_HUBER_D0_COV_SKATERS + \
                 EWA_PM_EMP_D0_COV_SKATERS + \
                 EWA_LW_D0_COV_SKATERS+\
                 EWA_LZ_D0_COV_SKATERS+\
                 WEAK_EWA_DO_COV_SKATERS+\
                 WEAK_PM_DO_COV_SKATERS+\
                 WEAK_LZ_DO_COV_SKATERS+\
                 WEAK_SK_DO_COV_SKATERS


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


def cov_skater_manifest():
    from precise.whereami import url_from_skater_name
    return dict([(f.__name__, url_from_skater_name(f.__name__)) for f in ALL_COV_SKATERS])


def random_cov_skater():
    return random.choice(ALL_D0_SKATERS)


def cov_skater_manifest_markdown():
    manifest = cov_skater_manifest()
    data = [ {'covariance skater':mgr,'location':url} for mgr, url in manifest.items() ]
    markdown = Tomark.table(data)
    return markdown


def write_cov_skater_manifest():
    markdown = cov_skater_manifest_markdown()
    with open(COV_SKATER_MANIFEST,'wt') as fh:
        fh.write(markdown)


if __name__=='__main__':
    from pprint import pprint
    pprint(cov_skater_manifest())
    write_cov_skater_manifest()