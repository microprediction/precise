from precise.skaters.covarianceutil.covfunctions import try_invert, cov_distance
import numpy as np
from precise.skaters.portfoliostatic.equalport import equal_long_port


def conjugate_with_seriation(seriator, port, seriator_kwargs=None, port_kwargs:dict=None, cov=None, pre=None)->np.ndarray:
    """
         A helper for conjugating seriation with any portfolio method

    :param seriator:          Takes a distance matrix and returns an ordering
    :param port:              Portfolio generator
    :param port_kwargs:       Arguments to portfolio generator, other than 'cov' and/or 'pre'
    :param cov:               Original portfolio in arbitrary order
    :param pre:               Original precision matrix in arbitrary order
    :return: w                Portfolio weights in original ordering
    """
    if seriator_kwargs is None:
        seriator_kwargs = {}

    if cov is None:
        cov = try_invert(pre)

    if port_kwargs is None:
        port_kwargs = {}

    if any(np.diag(cov)<1e-6):
        return equal_long_port(cov=cov)
    elif seriator is None:
        w = port(cov=cov, **port_kwargs)
        return np.array(w)
    else:
        # Establish ordering using seriator and corr distances
        cov_dist = cov_distance(cov)
        ndx = seriator(cov_dist, **seriator_kwargs)
        inv_ndx = np.argsort(ndx)
        cov_cols = cov[:,ndx]
        cov_back = cov_cols[:,inv_ndx]
        assert np.allclose(cov,cov_back)
        ordered_cov = cov_cols[ndx,:]

        # Allocate capital to ordered assets
        ordered_w = port(cov=ordered_cov, **port_kwargs)

        # Return to original ordering
        try:
            w = ordered_w[inv_ndx]
        except TypeError:
            print('Warning: '+port.__name__+' returns list not array - should really fix this ')
            w = np.array(ordered_w)[inv_ndx]
        return np.array(w)