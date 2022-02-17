from precise.skaters.covariance.buffactory import _buf
import pandas as pd
import numpy as np

# Thin wrapper for some Riskfolio-Lib methods
# For full flexibility refer to the package https://github.com/dcajasn/Riskfolio-Lib/blob/master/examples


RPL_RISK_METRICS = ['vol', 'MV', 'MAD', 'MSV', 'FLPM', 'SLPM',
       'VaR','CVaR', 'EVaR', 'WR', 'MDD', 'ADD',
       'DaR', 'CDaR', 'EDaR', 'UCI', 'MDD_Rel', 'ADD_Rel',
       'DaR_Rel', 'CDaR_Rel', 'EDaR_Rel', 'UCI_Rel']


def rfl_hrp_factory(s, y, k=1, metric='MV', n_buffer:int=100, e=1):
    """
         Hierarchical Risk Parity
    """
    assert metric in RPL_RISK_METRICS, metric+' is not a valid RPL_RISK_METRIC '
    optim_kwargs = {'rm':metric,'model':'HRP'}
    return rpl_manager_factory(s=s, y=y, k=k, e=e, cls_name='HCPortfolio', n_buffer=n_buffer, optim_kwargs=optim_kwargs)


def rpl_manager_factory(s, y, k=1, e=1, cls_name='HCPortfolio', optim_kwargs:dict=None, n_buffer:int=1000):
    """
         Applies riskfolio-lib routines to buffer
    """
    fun_kwargs = {'rp_optim_kwargs': optim_kwargs}
    fun_kwargs.update({'port_cls_name': cls_name})
    s = _buf(funcs=[_rpl_func], func_names=['weights'], func_kwargs=[fun_kwargs], s=s, x=y,
                e=e, n_buffer=n_buffer)
    w = s.get('weights')
    if w is None:
        w = np.ones(len(y))
    return w, s


def _rpl_func(xs, port_cls_name, rp_optim_kwargs:dict=None):
    import riskfolio as rp
    if rp_optim_kwargs is None:
        rp_optim_kwargs = {}
    returns = pd.DataFrame(data=xs)
    try:
        portfolio_cls = getattr(rp, port_cls_name)
    except:
        raise ValueError(port_cls_name+' is not a valid class name in riskfolio-lib')
    port = portfolio_cls(returns=returns)
    w_dict = port.optimization(**rp_optim_kwargs)
    w = w_dict['weights'].values
    return w





