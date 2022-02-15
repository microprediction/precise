from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
from precise.skaters.covarianceutil.statemutations import both_cov

def test_manifesto():
    from precise.skaters.covariance.allcovskaters import cov_skater_manifest
    stuff = cov_skater_manifest()


def test_emp():
    ys = create_correlated_dataset(n=500)
    s = {}
    for y in ys:
        x, x_cov, s = run_emp_pcov_d0(s=s, y=y)
    pcorr = cov_to_corrcoef(x_cov)
    pprint(pcorr)  # Population correlation
    ys = create_correlated_dataset(n=500)
    s = {}
    for y in ys:
        x, x_cov, s = run_emp_pcov_d0(s=s, y=y)
    pprint(s)

    ys = create_correlated_dataset(n=500)
    s = {}
    for y in ys:
        x, x_cov, s = run_emp_pcov_d0(s=s, y=y)  # <---
    s = both_cov(s)  # <--- Peek in the state and converts scov to pcov
    scorr = cov_to_corrcoef(s['scov'])
    s = both_cov(s)  # <--- Converts scov to pcov
    pprint(s['scov'])
    pprint(s['scov'])



from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covariance.bufsk import buf_sk_oas_pcov_d0_n100
from precise.skaters.covariance.runemp import run_emp_pcov_d0
from precise.skaters.covarianceutil.statefunctions import oas
from pprint import pprint

# Basic show_em of running OAS covariance
# (just a simple function of the running state)


def test_oas():
    ys = create_correlated_dataset(n=50)

    # Method 1: Slow
    s1 = {}
    for y in ys[:3]:
        x, x_cov, s1 = buf_sk_oas_pcov_d0_n100(s=s1, y=y)
    print(x_cov)

    # Method 2: Use the empirical skater and, when you need it, apply the OAS helper
    # (Will be the same but only so long as n<n_buffer)
    s2 = {}
    for i,y in enumerate(ys):
        x, x_cov, s2 = run_emp_pcov_d0(s=s2, y=y)
    print(oas(**s2))  # <--- Lazy style often works for statefunctions
    print(oas(pcov=x_cov,n_samples=i+1) ) # <--- Explicit style