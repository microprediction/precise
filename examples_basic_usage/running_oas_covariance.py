from precise.skatertools.syntheticdata import create_correlated_dataset
from precise.skaters.covariance import emp_pcov
from pprint import pprint
from precise.skaters.covariance import oas

# Basic example of running OAS covariance
# (just a simple function of the running state)

if __name__=='__main__':
    xs = create_correlated_dataset(n=500)
    s = {}
    for x in xs:
        s = emp_pcov(s=s, x=x)
    cov_style_1 = oas(pcov=s['pcov'],n_samples=s['n_samples'])
    cov_style_2 = oas(**s)      # <--- State functions can also be called this lazy way
    pprint(cov_style_1)
    pprint(cov_style_2)

