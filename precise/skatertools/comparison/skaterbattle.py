from precise.skaters.covariance.allcovskaters import ALL_D0_SKATERS
from precise.skatertools.data.skaterresiduals import random_multivariate_residual
from precise.skaters.covarianceutil.likelihood import cov_skater_loglikelihood
from uuid import uuid4
import os
import json
import pathlib
import numpy as np
from pprint import pprint
import traceback
from collections import Counter
from momentum.functions import rvar
from precise.skatertools.data.equity import random_m6_returns
from precise.whereami import SKATER_WIN_DATA

# Creates a new file to put on the skater win data queue

params = {'n_dim': 25,
          'n_obs': 160,
          'n_burn':140,
          'atol': 1e-4,
          'lb':-1000,
          'ub':1000,
          'interval':'d'}

descriptions = {'m':'equity_monthly',
                'd':'equity_daily'}

params['description'] = descriptions[params['interval']]

if __name__=='__main__':
    atol = 1.0
    pprint(ALL_D0_SKATERS)
    category = params['description']+'_p'+str(params['n_dim'])+'_n'+str(params['n_burn'])
    qn = str(uuid4())+'.json'
    queue_dir = os.path.join(SKATER_WIN_DATA, category)
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
    interval = params['interval']

    while True:
        n_dim = params['n_dim']
        n_obs = params['n_obs']
        xs = random_m6_returns(n_dim=n_dim, n_obs=n_obs, verbose=False, interval=interval)
        assert len(xs)==n_obs
        xs = np.array(xs)
        np.random.shuffle(ALL_D0_SKATERS)
        fs = ALL_D0_SKATERS[:3]
        stuff = list()

        for f in fs:
            try:
                ll, metrics = cov_skater_loglikelihood(f=f, xs=xs, n_burn=params['n_burn'], with_metrics=True, lb=lb, ub=ub)
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













