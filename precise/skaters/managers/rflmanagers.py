from precise.skaters.managers.rflmanagerfactory import rfl_hrp_factory


# Risk Measures available in RiskFolio-Lib
# (See this example https://nbviewer.org/github/dcajasn/Riskfolio-Lib/blob/master/examples/Tutorial%2024.ipynb)
#
# 'vol': Standard Deviation.
# 'MV': Variance.
# 'MAD': Mean Absolute Deviation.
# 'MSV': Semi Standard Deviation.
# 'FLPM': First Lower Partial Moment (Omega Ratio).
# 'SLPM': Second Lower Partial Moment (Sortino Ratio).
# 'VaR': Conditional Value at Risk.
# 'CVaR': Conditional Value at Risk.
# 'EVaR': Entropic Value at Risk.
# 'WR': Worst Realization (Minimax)
# 'MDD': Maximum Drawdown of uncompounded cumulative returns (Calmar Ratio).
# 'ADD': Average Drawdown of uncompounded cumulative returns.
# 'DaR': Drawdown at Risk of uncompounded cumulative returns.
# 'CDaR': Conditional Drawdown at Risk of uncompounded cumulative returns.
# 'EDaR': Entropic Drawdown at Risk of uncompounded cumulative returns.
# 'UCI': Ulcer Index of uncompounded cumulative returns.
# 'MDD_Rel': Maximum Drawdown of compounded cumulative returns (Calmar Ratio).
# 'ADD_Rel': Average Drawdown of compounded cumulative returns.
# 'DaR_Rel': Drawdown at Risk of compounded cumulative returns.
# 'CDaR_Rel': Conditional Drawdown at Risk of compounded cumulative returns.
# 'EDaR_Rel': Entropic Drawdown at Risk of compounded cumulative returns.
# 'UCI_Rel': Ulcer Index of compounded cumulative returns.


def rfl_hrp_var_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='MV', n_buffer=200)


def rfl_hrp_vol_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='vol', n_buffer=200)


def rfl_hrp_mad_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='MAD', n_buffer=200)


def rfl_hrp_msv_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='MSV', n_buffer=200)


def rfl_hrp_flpm_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='FLPM', n_buffer=200)


def rfl_hrp_slpm_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='SLPM', n_buffer=200)


def rfl_hrp_var_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='VaR', n_buffer=200)


def rfl_hrp_cvar_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='CVaR', n_buffer=200)


def rfl_hrp_evar_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='EVaR', n_buffer=200)


def rfl_hrp_wr_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='WR', n_buffer=200)


def rfl_hrp_mdd_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='MDD', n_buffer=200)


def rfl_hrp_add_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='ADD', n_buffer=200)


def rfl_hrp_dar_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='DaR', n_buffer=200)


def rfl_hrp_cdar_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='CDaR', n_buffer=200)


def rfl_hrp_edar_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='EDaR', n_buffer=200)


def rfl_hrp_mddrel_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='MDD_Rel', n_buffer=200)


def rfl_hrp_addrel_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='ADD_Rel', n_buffer=200)


def rfl_hrp_cdarrel_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='CDaR_Rel', n_buffer=200)


def rfl_hrp_edarrel_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='EDaR_Rel', n_buffer=200)


def rfl_hrp_ucirel_long_manager_n200(y, s, k=1, e=1, **ignore):
    return rfl_hrp_factory(y=y, s=s, k=k, e=e, metric='UCI_Rel', n_buffer=200)


RFL_HRP_LONG_MANAGERS = [rfl_hrp_var_long_manager_n200, rfl_hrp_vol_long_manager_n200,
                         rfl_hrp_mad_long_manager_n200, rfl_hrp_msv_long_manager_n200,
                         rfl_hrp_flpm_long_manager_n200, rfl_hrp_slpm_long_manager_n200,
                         rfl_hrp_var_long_manager_n200, rfl_hrp_cvar_long_manager_n200,
                         rfl_hrp_evar_long_manager_n200, rfl_hrp_wr_long_manager_n200,
                         rfl_hrp_mdd_long_manager_n200, rfl_hrp_add_long_manager_n200,
                         rfl_hrp_dar_long_manager_n200, rfl_hrp_cdar_long_manager_n200,
                         rfl_hrp_edar_long_manager_n200, rfl_hrp_mddrel_long_manager_n200,
                         rfl_hrp_addrel_long_manager_n200, rfl_hrp_cdarrel_long_manager_n200,
                         rfl_hrp_edarrel_long_manager_n200, rfl_hrp_ucirel_long_manager_n200]

RFL_HRP_LS_MANAGERS = []
RFL_HRP_MANAGERS = RFL_HRP_LONG_MANAGERS + RFL_HRP_LS_MANAGERS

RFL_LONG_MANAGERS = RFL_HRP_LONG_MANAGERS
RFL_LS_MANAGERS = RFL_HRP_LS_MANAGERS



