from precise.skatertools.data.skaterresiduals import random_multivariate_residual, random_noncollinear_residual
from precise.skatervaluation.battledata.sourceconventions import verify_source_outputs
import numpy as np


DEFAULT_TM_PARAMS = {'n_dim': 25,
                      'n_obs': 356,
                      'n_burn':300,
                      'atol': 1,
                      'raw':1,
                      'lb':-1000,
                      'ub':1000}


def tm_source(params)->(dict, str, np.ndarray):
    """
        Retrieve from a cache of time-series models residuals in the precisedata GitHub repo

        params['collinear'] - If not True, we first create a less-collinear set of residuals

    """
    combined_params = DEFAULT_TM_PARAMS
    combined_params.update(params)
    combined_params['description'] = 'tm_residuals' if combined_params['raw'] else 'tm_noncollinear'
    category = combined_params['description'] + '_p' + str(combined_params['n_dim']) + '_n' + str( combined_params['n_burn'])
    if combined_params['raw']:
        xs = random_multivariate_residual(n_obs=combined_params['n_obs'], as_dataframe=False, random_start=True)
    else:
        xs = random_noncollinear_residual(n_obs=combined_params['n_obs'], random_start=True)
    verify_source_outputs((combined_params,category,xs))
    return combined_params, category, xs