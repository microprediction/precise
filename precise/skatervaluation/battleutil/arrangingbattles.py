from precise.skaters.covariance.allcovskaters import ALL_D0_SKATERS
from precise.skaters.covarianceutil.likelihood import cov_skater_loglikelihood
from uuid import uuid4
import os
import json
import pathlib
from pprint import pprint
import traceback
from collections import Counter
from momentum.functions import rvar
from precise.skatertools.data.equity import random_m6_returns
from precise.whereami import BATTLE_RESULTS_DIR
import numpy as np
import time


DEFAULT_M6_PARAMS = {'n_dim': 25,
                      'n_obs': 356,
                      'n_burn':300,
                      'atol': 1,
                      'lb':-1000,
                      'ub':1000,
                      'interval':'d',
                      'etfs':0}


def params_category_and_data(params:dict):
    """
         Supplement params (usually inferred from battle script file names) with defaults
    """
    if params['topic']== 'm6':
        combined_params = DEFAULT_M6_PARAMS
        combined_params.update(params)
        descriptions = {'m': 'm6_stocks_monthly',
                        'd': 'm6_stocks_daily'} if not params['etf'] else {'m': 'm6_monthly',
                                                                           'd': 'm6_daily'}
        combined_params['description'] = descriptions[combined_params['interval']]
        category = combined_params['description'] + '_p' + str(combined_params['n_dim']) + '_n' + str(combined_params['n_burn'])
        xs = random_m6_returns(verbose=False, **combined_params)
        return combined_params, category, xs
    else:
        raise ValueError('m6 is only topic, for now')


def skater_likelihood_battle(params:dict):
    """
    :param
    :return:
    """
    return skater_battle(evaluator=cov_skater_loglikelihood, evaluator_name='likelihood', params=params)


def skater_battle(evaluator, evaluator_name:str, params:dict):
    """
        Write results to a new queue.
        evaluator(f=f, xs=xs, n_burn=params['n_burn'], with_metrics=True, lb=lb, ub=ub)
    """
    n_per_battle = 3
    atol = 1.0
    try:
        params, category, xs_test = params_category_and_data(params=params)
    except Exception as e:
        print(e)
        pprint(params)
        print('Something is probably wrong with params for getting data, so this config will not fly')
        params, category, xs_test = params_category_and_data(params=params)

    print('Data retrieval test passed for category '+category)
    pprint(params)
    time.sleep(1)
    print('Will test the following skaters')
    pprint(ALL_D0_SKATERS)

    qn = str(uuid4())+'.json'
    queue_dir = os.path.join(BATTLE_RESULTS_DIR, evaluator_name, category)
    queue = os.path.join(queue_dir,qn)
    pathlib.Path(queue_dir).mkdir(parents=True, exist_ok=True)
    print(queue)

    battles = Counter()
    timing = dict()
    reliability = dict()
    failures = dict()

    worst_ll_seen = 10000000
    lb = params['lb']
    ub = params['ub']

    while True:
        n_obs = params['n_obs']
        params, category, xs = params_category_and_data(params=params)
        assert len(xs)==n_obs
        xs = np.array(xs)
        np.random.shuffle(ALL_D0_SKATERS)
        fs = ALL_D0_SKATERS[:n_per_battle]
        stuff = list()

        for f in fs:
            try:
                ll, metrics = evaluator(f=f, xs=xs, n_burn=params['n_burn'], with_metrics=True, lb=lb, ub=ub)
                metrics['name']=f.__name__
                metrics['traceback']=''
                metrics['passing']=1
                stuff.append( (ll,metrics) )
                if ll<worst_ll_seen:
                    worst_ll_seen = ll
                    print({'worst_ll_seen':ll})
                name = metrics['name']
                if name not in timing:
                    timing[name] = {}
                timing[name] = rvar(timing[name], x=metrics['time'], rho=0.05)
                if name not in reliability:
                    reliability[name] = {}
                reliability[name] = rvar(reliability[name], x=1.0, rho=0.05)
            except Exception as e:
                metrics = {'name':f.__name__,'passing':0,'traceback':traceback.format_exc(),'ll':-100000000}
                if f.__name__ not in reliability:
                    reliability[f.__name__] = {}
                reliability[f.__name__] = rvar(reliability[f.__name__], x=0.0, rho=0.05)
                failures[f.__name__] = traceback.format_exc()
                ll = worst_ll_seen
            stuff.append( (ll,metrics))
        valid = [ s for s in stuff if s[1]['passing']>0.5 ]

        if len(valid)<=2:
            print('urhg')

        for i, mi in enumerate(valid):
            for j, mj in enumerate(valid):
                if j != i:
                    if mi[0] > mj[0]+atol:
                        i_name = mi[1]['name']
                        j_name = mj[1]['name']
                        cmp_name = i_name+'>'+j_name
                        battles.update({cmp_name:1.0})

        reliabilties = dict([(nm, reliab['mean']) for nm,reliab in reliability.items() ] )
        cpu_times = dict([(nm, tm['mean']) for nm, tm in timing.items()])

        if np.random.rand()<0.01:
            with open(queue,'wt') as fh:
                json.dump(battles,fh)
                print('---')
                pprint(reliabilties)
                print('---')
                pprint(cpu_times)
                print('---')
                pprint(battles)
                print(' ')
                pprint(failures)













