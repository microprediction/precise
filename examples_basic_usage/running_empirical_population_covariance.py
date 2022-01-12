from precise.synthetic.generate import create_correlated_dataset
from precise.covariance.empirical import emp_pcov
from pprint import pprint

# Basic example of running empirical population covariance

if __name__=='__main__':
    xs = create_correlated_dataset(n=500)
    ocov = {}
    for x in xs:
        ocov = emp_pcov(s=ocov, x=x)
    pprint(ocov)
