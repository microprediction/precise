from precise.synthetic.generate import create_correlated_dataset
from precise.covariance.empirical import emp_pcov
from pprint import pprint
from precise.covariance.matrixfunctions import cov_to_corrcoef

# Basic example of running empirical population correlation

if __name__=='__main__':
    xs = create_correlated_dataset(n=500)
    s = {}
    for x in xs:
        s = emp_pcov(s=s, x=x)
    pcorr = cov_to_corrcoef(s['pcov'])
    pprint(pcorr)    # Population correlation
