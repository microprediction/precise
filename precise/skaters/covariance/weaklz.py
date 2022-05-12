from precise.skaters.covariance.weakfactory import weak_pcov_factory
from precise.skaters.covariance.ewalz import ewa_lz_scov_d0_r005_l010_n100, ewa_lz_scov_d0_r005_l020_n50, ewa_lz_scov_d0_r010_l010_n100

# Using structure learning


def weak_lz_scov_d0_r005_l010_n100(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_lz_scov_d0_r005_l010_n100, s=s, y=y, k=k, e=e)


def weak_lz_scov_d0_r005_l020_n50(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_lz_scov_d0_r005_l020_n50, s=s, y=y, k=k, e=e)


def weak_lz_scov_d0_r010_l010_n100(s, y, k=1, e=1):
    return weak_pcov_factory(f=ewa_lz_scov_d0_r010_l010_n100, s=s, y=y, k=k, e=e)



WEAK_LZ_DO_COV_SKATERS = [weak_lz_scov_d0_r010_l010_n100, weak_lz_scov_d0_r005_l020_n50, weak_lz_scov_d0_r010_l010_n100]