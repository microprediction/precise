from precise.synthetic.generate import create_correlated_dataset
from precise.covariance.empirical import emp_pcov
from pprint import pprint
from precise.covariance.util import both_cov

# Basic example of running empirical population covariance

if __name__=='__main__':
    xs = create_correlated_dataset(n=500)
    s = {}
    for x in xs:
        s = emp_pcov(s=s, x=x)
    s = both_cov(s)  # <--- Converts scov to pcov
    pprint(s['scov'])
