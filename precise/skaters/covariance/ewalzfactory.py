import numpy as np
from precise.skaters.covarianceutil.adjacency import centroid_precision_adjacency
from precise.skaters.covarianceutil.covfunctions import affine_inversion
from precise.skaters.covariance.ewaemp import ewa_emp_pcov_factory

# A factory for approaches that utilize episodically estimated sparsity in precision matrix.
# Yielding a family of autonomous algorithms inspired by a paper by Lee and Zhong

#  Algorithm steps and defaults
#  ----------------------------
#  1. A global cov matrix is maintained  (ewa_pcov)
#  2. A buffer of past observations is maintained
#  3. Each epoch an adjacency matrix for precision is estimated from the global cov (centroid method)
#  4. Local pre models are re-booted, assuming the new structure (ewa_pcov)
#  5. At any time a global pre matrix can be computed from local pre matrices (affine inversion)
#  6. At any time a global cov matrix can be computed by inverting global pre (affine inversion)

# Here are the defaults:

# Step 1
default_f_global = ewa_emp_pcov_factory
DEFAULT_F_GLOBAL_KWARGS = {'r':0.01}

# Step 2
DEFAULT_N_EPOCH = 100

# Step 3
def default_adjacency_func(cov, phi=1.01, lmbd=0.01):
    """ Default way to specify sparsity in precision matrix
    :param cov: (n_dim, n_dim)
    :return: (n_dim, n_dim) bool
    """
    pre = affine_inversion(a=cov, phi=phi, lmbd=lmbd)
    return centroid_precision_adjacency(pre=pre)
DEFAULT_ADJ_FUNC_KWARGS = {'phi':1.01,'lmbd':0.01}


# Step 4
default_f_local = ewa_emp_pcov_factory
DEFAULT_F_LOCAL_KWARGS = {'r':0.01}

# Step 5
def default_local_pre_func(cov, phi, lmbd):
    """ Default way to invert local cov matrices
    """
    return affine_inversion(a=cov, phi=phi, lmbd=lmbd)
DEFAULT_LOCAL_PRE_FUNC_KWARGS = {'phi':1.1,'lmbd':0.1}

# Step 6
default_global_cov_func = default_local_pre_func
DEFAULT_GLOBAL_COV_FUNC_KWARGS = {'phi':1.01,'lmbd':0.1}


def ewa_emp_lz_pcov_factory_rg_rl_n(y, s, rg, rl, n, e):
    """
    :param y:
    :param s:
    :param n_epoch:     Length of epoch
    :param rg:
    :param rl:
    :param e:
    :return:
    """
    f_global_kwargs = {'r':rg}
    f_local_kwargs = {'r':rl}
    return lz_factory(y=y,s=s,n_epoch=n,
                      f_local =  ewa_emp_pcov_factory,
                      f_global = ewa_emp_pcov_factory,
                      f_global_kwargs=f_global_kwargs,
                      f_local_kwargs=f_local_kwargs,
                      e=e)


def lz_factory(y, s:dict, n_epoch=DEFAULT_N_EPOCH,
               f_global=None, f_global_kwargs=None,
               f_local=None, f_local_kwargs=None,
               e=1,
               adj_func=None, adj_func_kwargs:dict=None,
               local_pre_func=None, local_pre_func_kwargs:dict=None,
               global_cov_func=None, global_cov_func_kwargs:dict=None):
    """

      Le and Zhong factory

    :param y:                Vector of observations
    :param s:                State
    :param n_epoch:          Length of epoch during which adjacency matrix is held constant
    :param f_global:         Skater maintaining a global estimate of covariance
    :param f_local:          Skater used to maintain n_dim local estimates, one for each variable
    :param e:                Set <0 to skip global cov, pre calculations
    :param adj_func:         Takes pre matrix and returns binary of same shape (where non-zeros should go)
    :param local_pre_func:   Function to take local cov matrices and produce precision matrices
    :param global_cov_func:  Function to take global precision matrix and produce global cov matrix
    :return: x, x_cov, s
    """

    # Mildly tedious stuff...
    if adj_func is None:
        adj_func = default_adjacency_func
    if local_pre_func is None:
        local_pre_func = default_local_pre_func
    if global_cov_func is None:
        global_cov_func = default_global_cov_func
    if adj_func_kwargs is None:
        adj_func_kwargs = DEFAULT_ADJ_FUNC_KWARGS
    if local_pre_func_kwargs is None:
        local_pre_func_kwargs = DEFAULT_LOCAL_PRE_FUNC_KWARGS
    if global_cov_func_kwargs is None:
        global_cov_func_kwargs = DEFAULT_GLOBAL_COV_FUNC_KWARGS

    if f_global_kwargs is None:
        f_global_kwargs = {}
    if f_local_kwargs is None:
        f_local_kwargs = {}

    # Initialization of global state s['g'] and local states s['l']['states']
    n_dim = len(y)
    if not s:
        s = {'g':{},          # Global state
             'l':{'states':[{} for _ in range(n_dim)]}, # Local states
             'buffer':[],     # Observation buffer
             'count':0,
             'warm':0,        # Local models are primed
             'stale':0}       # Global pre/cov is stale

    # Maintain a global covariance model
    s['count'] += 1
    x_gl, gl_cov, s['g'] = f_global(s=s['g'], y=y, **f_global_kwargs)
    if s['count'] % n_epoch == 0:
        # Trigger adjacency matrix discovery from the global model
        s['l']['adj'] = adj_func(gl_cov, **adj_func_kwargs)

        # Prepare the "B" matrices in the paper
        s['l']['n_dims'] = [int(s) for s in np.sum(s['l']['adj'], axis=0)]
        s['l']['bs'] = dict()
        for i, nd in enumerate(s['l']['n_dims']):
            b_ = np.zeros(shape=(n_dim, nd))
            ndxs = s['l']['adj'][:, i]
            b_[ndxs, :] = np.eye(nd)
            s['l']['bs'][i] = b_

        # Reset local states ...
        s['l']['states'] = [{} for _ in range(n_dim)]
        #  ... but replay data from the buffer through local states once
        for i in range(n_dim):
            ls = {}
            indx = s['l']['adj'][:, i]
            for yt in s['buffer']:
                yti = yt[indx]
                xl, xl_cov, ls = f_local(s=ls,y=yti, **f_local_kwargs )
            s['l']['states'][i] = ls

        # Blow away the buffer and declare it ready
        s['buffer'] = []
        s['warm'] = 1

    # Add current data vector to buffer
    s['buffer'].append(y)
    if len(s['buffer'])>n_epoch:
        s['buffer'].pop(0)

    # If local models are initialized, process one data point
    if s['warm']:
        # Update local states and most recent cov estimates
        s['l']['covs'] = [ None for _ in range(n_dim) ]
        for i in range(n_dim):
            indx = s['l']['adj'][:, i]
            yi = y[indx]
            sl = s['l']['states'][i]
            _, s['l']['covs'][i], sl = f_local(s=sl, y=yi, **f_local_kwargs)
            s['l']['states'][i] = sl



    # If allowed time, compute precision and covariance
    #  - User can set e<0 to skip this step)
    #  - User can supply a "fake" global_cov_func to avoid that overhead, if they want
    if s['warm']:
        if (e>=0):
                # Reconstruct precision - see paper for explanation
                omega = np.eye(n_dim)
                for i,covi in enumerate(s['l']['covs']):
                    prei = local_pre_func(covi, **local_pre_func_kwargs)
                    ei = np.zeros(shape=(n_dim,1))
                    ei[i] = 1.0
                    bi = s['l']['bs'][i]
                    fi = np.matmul(bi.T,ei)
                    Sfi = np.matmul(prei,fi)
                    wi = np.matmul(bi,Sfi)
                    omega[:,i] = wi[:,0]
                s['pre'] = omega
                s['cov'] = global_cov_func(omega,**global_cov_func_kwargs)
                s['stale']=0
        else:
            s['stale']=1

    # Return cov is fresh, else fall back to global model
    if (not s['warm']) or s['stale']:
        return x_gl, gl_cov, s
    else:
        return x_gl, s['cov'], s













