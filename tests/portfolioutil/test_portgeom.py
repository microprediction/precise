import random
from precise.skaters.portfolioutil.portgeometry import verbosely_choose_close_point_on_boundary_of_convex_hull
import numpy as np


def test_geom():
    n_dim = random.choice([1,2,500])
    n_port = random.choice([1 ,2 ,25])
    x1 = np.random.randn(n_dim)
    xs = [ xi +x1 for xi in np.random.randn(n_port ,n_dim) ]
    x = verbosely_choose_close_point_on_boundary_of_convex_hull(xs, verbose=True)


if __name__=='__main__':
    for _ in range(20):
        test_geom()
