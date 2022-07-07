from precise.skatertools.data.equityhistorical import random_cached_equity_dense
import traceback
import os
from uuid import uuid4
import json
from pprint import pprint
from precise.whereami import TESTSERROR
import pathlib
import time


def manager_test_run(mgr,n_obs=50,n_dim=7, j=1, q=1.0, verbose=False):
    """
       Test manager and log traceback to /testserrors
    """
    xs = random_cached_equity_dense(k=1, n_obs=n_obs, n_dim=n_dim, as_frame=False)

    try:
        s = {}
        if verbose:
            print('Manager test run burn-in phase starting ')
        for y in xs[:n_obs - 5]:
            w, s = mgr(y=y, s=s, e=-1, j=j, q=q)

        if verbose:
            print('Manager test run usage phase starting ')
        for y in xs[-5:]:
            w, s = mgr(y=y, s=s, e=1, j=j, q=q)
    except Exception as e:
        error_data = {'traceback':traceback.format_exc(),
         'exception':str(e),
         'manager':mgr.__name__}
        manager_error_dir = os.path.join(TESTSERROR,'managers')
        pathlib.Path(manager_error_dir).mkdir(parents=True, exist_ok=True)
        error_file = os.path.join(manager_error_dir,mgr.__name__+'_'+str(uuid4())+'.json')
        pprint(error_data)
        with open(error_file, 'wt') as fh:
            json.dump(error_data,fh)
    return w


def manager_profile(mgr,n_obs=500,n_dim=50, j=1, q=1.0, verbose=False):
    """
       Test manager and log traceback to /testserrors
    """
    xs = random_cached_equity_dense(k=1, n_obs=n_obs, n_dim=n_dim, as_frame=False)

    cpu = {-1:0,0:0,1:0}

    s = {}

    for e in [-1,0,1]:
        print(e)
        st = time.time()
        for y in xs[:25]:
            w, s = mgr(y=y, s=s, e=e, j=j, q=q)
        cpu[e]+= time.time()-st

    return cpu



if __name__=='__main__':
    from precise.skaters.managers.schurmanagers import schur_weak_weak_pm_t0_r025_n50_s25_g100_h125_long_manager as mgr
    cpu = manager_profile(mgr=mgr)
    pprint(cpu)