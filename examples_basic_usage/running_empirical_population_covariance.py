from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covariance.runemp import run_emp_pcov_d0
from pprint import pprint

# Basic show_em of running empirical population covariance

if __name__=='__main__':
    ys = create_correlated_dataset(n=500)
    s = {}
    for y in ys:
        x, x_cov, s = run_emp_pcov_d0(s=s, y=y)
    pprint(s)
