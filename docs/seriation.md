# Seriation
Reordering assets. If *xs* contains one column per variable:

    from precise.skaters.covarianceutil.covfunctions import seriation
    import numpy as np
    cov = np.cov(xs, rowvar=False)
    ndx = seriation(cov=cov)


See [example](https://github.com/microprediction/precise/blob/main/examples_seriation/metals_seriation.py)
  
-+-

Documentation [home](https://microprediction.github.io/precise)


View as [source](https://github.com/microprediction/precise/blob/master/docs/seriation.md) or [web](https://microprediction.github.io/precise/seriation)
