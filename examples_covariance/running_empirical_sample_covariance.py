from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covariance.runemp import run_emp_pcov_d0
from pprint import pprint
from precise.skaters.covarianceutil.statemutations import both_cov

# Basic show_em of running empirical population covariancecomparisonutil

if __name__=='__main__':
    ys = create_correlated_dataset(n=500)
    s = {}
    for y in ys:
        x, x_cov, s = run_emp_pcov_d0(s=s, y=y)
    s = both_cov(s)  # <--- Converts scov to pcov
    pprint(s['scov'])
