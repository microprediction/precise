from precise.skatertools.data.preciousmetalsreturns import precious_metals_returns
from precise.skaters.covarianceutil.covfunctions import seriation
import numpy as np

# Example of ordering assets

if __name__ == '__main__':
    xs = precious_metals_returns()
    cov = np.cov(xs, rowvar=False)
    ndx = seriation(cov=cov)
    print(ndx)
