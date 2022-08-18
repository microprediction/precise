# Using the portfolio functions

1. Choose a "port" by browsing [portfoliostatic](https://github.com/microprediction/precise/tree/main/precise/skaters/portfoliostatic).
2. Import it
3. Pass it either a covariance or a precision matrix

### Example usage
We need a cov matrix

       import numpy as np
       cov = np.array([[ 1.09948514, -1.02926114,  0.22402055,  0.10727343],
               [-1.02926114,  2.54302628,  1.05338531, -0.12481515],
               [ 0.22402055,  1.05338531,  1.79162765, -0.78962956],
               [ 0.10727343, -0.12481515, -0.78962956,  0.86316527]])

Then:

     from precise.skaters.portfoliostatic.unitport import unit_port
     w = unit_port(cov=cov)
     

-+-

Documentation [home](https://microprediction.github.io/precise)
