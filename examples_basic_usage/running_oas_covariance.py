from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covariance.bufsk import buf_sk_oas_pcov_d0_n100
from precise.skaters.covariance.runemp import run_emp_pcov_d0
from precise.skaters.covarianceutil.statefunctions import oas
from pprint import pprint

# Basic example of running OAS covariance
# (just a simple function of the running state)

if __name__=='__main__':
    ys = create_correlated_dataset(n=50)

    # Method 1: Use the buffered OAS skater
    s1 = {}
    for y in ys:
        x, x_cov, s1 = buf_sk_oas_pcov_d0_n100(s=s1, y=y)
    print(x_cov)

    # Method 2: Use the empirical skater and, when you need it, apply the OAS helper
    # (Will be the same but only so long as n<n_buffer)
    s2 = {}
    for i,y in enumerate(ys):
        x, x_cov, s2 = run_emp_pcov_d0(s=s2, y=y)
    print(oas(**s2))  # <--- Lazy style often works for statefunctions
    print(oas(pcov=x_cov,n_samples=i+1) ) # <--- Explicit style





