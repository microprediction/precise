from precise.synthetic.generate import create_correlated_dataset
from precise.covariance.empirical import emp_pcov
from pprint import pprint
from precise.covariance.util import ledoit_wolf

# Basic example of running Ledoit-Wolf covariance

if __name__=='__main__':
    xs = create_correlated_dataset(n=500)
    s = {}
    for x in xs:
        s = emp_pcov(s=s, x=x)
    ld = ledoit_wolf(s['pcov'],n_samples=s['n_samples'])

