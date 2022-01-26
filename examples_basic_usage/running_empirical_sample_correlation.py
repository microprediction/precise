from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covariance.runemp import run_emp_pcov_d0
from pprint import pprint
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
from precise.skaters.covarianceutil.statemutations import both_cov

# Basic example of running empirical sample correlation

if __name__=='__main__':
    ys = create_correlated_dataset(n=500)
    s = {}
    for y in ys:
        x, x_cov, s = run_emp_pcov_d0(s=s, y=y)  # <---
    s = both_cov(s)  # <--- Peek in the state and converts scov to pcov
    scorr = cov_to_corrcoef(s['scov'])
    pprint(scorr)    # Sample correlation
