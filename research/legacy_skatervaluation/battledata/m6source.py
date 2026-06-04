from precise.skatertools.data.equitylive import random_m6_returns, all_m6_returns
from precise.skatervaluation.battledata.sourceconventions import verify_source_outputs
import numpy as np


DEFAULT_M6_PARAMS = {'n_dim': 25,
                      'n_obs': 356,
                      'n_burn':300,
                      'atol': 1,
                      'lb':-1000,
                      'ub':1000,
                      'interval':'d',
                      'etf':1,
                      'implied':0}


def m6_source(params)->(dict, str, np.ndarray):
    """
         Slowly get up to date data via Yahoo
    """
    combined_params = DEFAULT_M6_PARAMS
    combined_params.update(params)
    etf = combined_params['etf']
    if etf>0.5:
        descriptions = {'m':'m6_monthly', 'd':'m6_daily'}
    elif etf<-0.5:
        descriptions = {'m': 'm6_etf_monthly', 'd': 'm6_etf_daily'}
    else:
        descriptions = {'m': 'm6_stocks_monthly', 'd': 'm6_stocks_daily'}

    combined_params['description'] = descriptions[combined_params['interval']]
    category = combined_params['description'] + '_p' + str(combined_params['n_dim']) + '_n' + str(
        combined_params['n_burn'])
    if params.get('implied'):
        category = category+'_implied'

    if combined_params['n_dim']<50:
        xs = random_m6_returns(verbose=False, **combined_params)
        verify_source_outputs((combined_params,category,xs))
    else:
        xs = all_m6_returns(verbose=False, **combined_params)
    return combined_params, category, xs


