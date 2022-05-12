from precise.skaters.covariance.weakfactory import weak_pcov_factory
from precise.skaters.covariance.bufsk import buf_sk_glcv_pcov_d0_n100_t0, buf_sk_lw_pcov_d0_n100, buf_sk_oas_pcov_d0_n100, buf_sk_mcd_pcov_d0_n100
# Using structure learning


def weak_sk_oas_pcov_d0_n100(s, y, k=1, e=1):
    return weak_pcov_factory(f=buf_sk_glcv_pcov_d0_n100_t0, s=s, y=y, k=k, e=e)


def weak_sk_lw_pcov_d0_n100(s, y, k=1, e=1):
    return weak_pcov_factory(f=buf_sk_lw_pcov_d0_n100, s=s, y=y, k=k, e=e)


def weak_sk_oas_pcov_d0_n100(s, y, k=1, e=1):
    return weak_pcov_factory(f=buf_sk_oas_pcov_d0_n100, s=s, y=y, k=k, e=e)


def weak_sk_mcd_pcov_d0_n100(s, y, k=1, e=1):
    return weak_pcov_factory(f=buf_sk_mcd_pcov_d0_n100, s=s, y=y, k=k, e=e)



WEAK_SK_DO_COV_SKATERS = [weak_sk_oas_pcov_d0_n100, weak_sk_lw_pcov_d0_n100,
                          weak_sk_oas_pcov_d0_n100, weak_sk_mcd_pcov_d0_n100]