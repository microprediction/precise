
from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.weakport import weak_long_port
from precise.skaters.portfoliostatic.unitport import unit_port
import numpy as np
from precise.skaters.locationutil.vectorfunctions import scatter
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef, nearest_pos_def, is_positive_def


def test_little_example():
    corr = np.array( [[1, -0.5, 0.3],
                     [-0.5, 1, 0.1],
                     [0.3, 0.1, 1]])
    sgma = np.array([1.0, 1.5, 2.0])
    cov = scatter(sgma)*corr
    corr1 = cov_to_corrcoef(cov)
    w1 = weak_portfolio_factory(cov=cov)

    cov2 = cov[:2,:2]
    w2 = unit_port(cov=cov2)
    w3 = weak_portfolio_factory(cov=cov2)


def test_bigger_example():
    from pprint import pprint
    corr = nearest_pos_def(np.array( [[1, -0.8, 0.3, 0.2],
                                     [-0.8, 1, 0.7, 0.3 ],
                                     [0.3, 0.7, 1, -0.8],
                                    [0.2, -0.3, -0.8, 1]]))
    sgma = np.array([1.0, 1.5, 1.25, 0.9])
    cov = scatter(sgma)*corr
    cov = nearest_pos_def(cov)
    pprint(cov)
    pprint(cov_to_corrcoef(cov))
    w0 = unit_port(cov=cov)
    print(w0)

    w1 = weak_portfolio_factory(cov=cov)

    print(w1)







if __name__=='__main__':
    test_bigger_example()