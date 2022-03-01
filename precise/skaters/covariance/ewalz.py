from precise.skaters.covariance.ewalzfactory import ewa_emp_lz_pcov_factory_rg_rl_n

# EWALZ short for "Exp Weight Avg Lee-Zhong"


def ewa_lz_scov_d0_r010_l010_n100(y, s, k=1, e=1):
    assert k==1
    return ewa_emp_lz_pcov_factory_rg_rl_n(y=y, s=s, rg=0.01, rl=0.01, n=100, e=e)


def ewa_lz_scov_d0_r005_l010_n100(y, s, k=1, e=1):
    assert k==1
    return ewa_emp_lz_pcov_factory_rg_rl_n(y=y, s=s, rg=0.005, rl=0.01, n=10, e=e)


def ewa_lz_scov_d0_r005_l020_n50(y, s, k=1, e=1):
    assert k==1
    return ewa_emp_lz_pcov_factory_rg_rl_n(y=y, s=s, rg=0.005, rl=0.02, n=50, e=e)



EWA_LZ_D0_COV_SKATERS = [ewa_lz_scov_d0_r010_l010_n100,
                         ewa_lz_scov_d0_r005_l010_n100,
                         ewa_lz_scov_d0_r005_l020_n50]

