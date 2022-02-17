from precise.skatertools.data.equityhistorical import random_cached_equity_dense
from precise.skatervaluation.battledata.sourceconventions import verify_source_outputs
import numpy as np

DEFAULT_STOCK_PARAMS = {'n_dim': 25,
                       'n_obs': 356,
                       'n_burn':300,
                       'atol': 1,
                       'lb':-1000,
                       'ub':1000,
                       'k':1}


def stocks_source(params)->(dict, str, np.ndarray):
    """
       Quickly get canned historical data from precisedata GitHub repo
    """
    combined_params = DEFAULT_STOCK_PARAMS
    combined_params.update(params)
    combined_params['description'] = 'stocks_' + str(combined_params['k']) + '_days'
    category = combined_params['description'] + '_p' + str(combined_params['n_dim']) + '_n' + str(
        combined_params['n_burn'])
    xs = random_cached_equity_dense(as_frame=False, **combined_params)
    verify_source_outputs((combined_params, category, xs))
    return combined_params, category, xs