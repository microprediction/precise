from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covariance.runemp import run_emp_pcov_d0 as f
from pprint import pprint

# Basic example of running empirical population covariance.
# This package contains dozens of alternatives to this particular choice of "f"

if __name__=='__main__':
    ys = create_correlated_dataset(n=500)
    s = {}
    for y in ys:
        x, x_cov, s = f(s=s, y=y)
    pprint(s)
