import numpy as np


def verify_source_outputs(outputs, n_dim=2):
    params, category, xs = outputs
    assert isinstance(category ,str)
    assert isinstance(params ,dict)
    assert np.shape(xs)[0 ] >20
    assert np.shape(xs)[1 ] >=n_dim
