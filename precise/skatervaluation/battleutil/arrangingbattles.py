from precise.skaters.covariance.allcovskaters import ALL_D0_SKATERS
from precise.skaters.managers.allmanagers import LONG_MANAGERS
from precise.skaters.covarianceutil.likelihood import cov_likelihood
from precise.skaters.managerutil.managerstats import manager_info, manager_var
from precise.skatervaluation.battledata.allsources import params_category_and_data
from uuid import uuid4
import os
import json
import pathlib
from pprint import pprint
import traceback
from collections import Counter
from momentum.functions import rvar
from precise.whereami import BATTLE_RESULTS_DIR
import numpy as np
import time


def manager_info_battle(params:dict):
    return generic_battle(contestants=LONG_MANAGERS, evaluator=manager_info, params=params, atol=1e-8)


def manager_var_battle(params:dict):
    return generic_battle(contestants=LONG_MANAGERS, evaluator=manager_var, params=params, atol=1e-8)


def cov_likelihood_battle(params:dict):
    contestants = ALL_D0_SKATERS
    return generic_battle(contestants=contestants, evaluator=cov_likelihood, params=params, atol=1.0)


def generic_battle(contestants, evaluator, params:dict, atol=1.0):
    """
        Write results to a new queue.
        evaluator(contestant=contestant, xs=xs, n_burn=params['n_burn'], with_metrics=True, lb=lb, ub=ub)
    """
    evaluator_name = evaluator.__name__
    n_per_battle = 7
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
    print('Will test the following contestants')
    pprint(contestants)

    qn = str(uuid4())+'.json'
    queue_dir = os.path.join(BATTLE_RESULTS_DIR, evaluator_name, category)
    queue = os.path.join(queue_dir,qn)
    pathlib.Path(queue_dir).mkdir(parents=True, exist_ok=True)
    print(queue)

    battles = Counter()
    timing = dict()
    reliability = dict()
    failures = dict()

    worst_assessment_seen = 10000000
    lb = params['lb']
    ub = params['ub']

    while True:
        n_obs = params['n_obs']
        params, category, xs = params_category_and_data(params=params)
        assert len(xs)==n_obs
        xs = np.array(xs)
        np.random.shuffle(contestants)
        some_contestants = contestants[:n_per_battle]

        stuff = list()
        for contestant in some_contestants:
            try:
                if 'manager' in contestant.__name__ or True:
                    print('  '+contestant.__name__)
                assessment, metrics = evaluator(contestant=contestant, xs=xs, n_burn=params['n_burn'], lb=lb, ub=ub)
                metrics['name']=contestant.__name__
                metrics['traceback']=''
                metrics['passing']=1
                if assessment<worst_assessment_seen:
                    worst_assessment_seen = assessment
                    print({'worst_assessment_yet':assessment})
                name = metrics['name']
                if name not in timing:
                    timing[name] = {}
                timing[name] = rvar(timing[name], x=metrics['time'], rho=0.05)
                if name not in reliability:
                    reliability[name] = {}
                reliability[name] = rvar(reliability[name], x=1.0, rho=0.05)
            except Exception as e:
                metrics = {'name':contestant.__name__,'passing':0,'traceback':traceback.format_exc(),'ll':-100000000}
                if contestant.__name__ not in reliability:
                    reliability[contestant.__name__] = {}
                reliability[contestant.__name__] = rvar(reliability[contestant.__name__], x=0.0, rho=0.05)
                failures[contestant.__name__] = traceback.format_exc()
                assessment = worst_assessment_seen
            stuff.append( (assessment,metrics))
        valid = [ s for s in stuff if s[1]['passing']>0.5 ]

        if len(valid)<=2:
            print('Less than 2 working contestants this time around: ')
            pprint(some_contestants)
            for contestant in some_contestants:
                pprint(failures.get(contestant.__name__))
            print('Urgh')

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

        if np.random.rand()<1:
            with open(queue,'wt') as fh:
                print('Saving')
                json.dump(battles,fh)
                print('---')
                pprint(reliabilties)
                print('---')
                pprint(battles)
                print(' ')
                pprint(failures)
                print('---')
                pprint(cpu_times)
            time.sleep(10)













