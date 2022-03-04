from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_ewa_manager_factory,schur_diag_diag_buf_emp_manager_factory


# Some Hierarchical Risk-Parity managers very loosely based on some literature


# Original Hierarchical Risk Parity approach
# (Note that seriation may be different so this is not supposed to be a replica)


def ldp_s5_n50_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=50, e=e, gamma=0, delta=0)


def ldp_s25_n50_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=50, e=e, gamma=0, delta=0)


def ldp_s5_n100_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0)


def ldp_s25_n100_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0)





LDP_LONG_MANAGERS = [ldp_s5_n50_long_manager, ldp_s25_n50_long_manager,
                     ldp_s5_n100_long_manager, ldp_s25_n100_long_manager
                     ]
HRP_LS_NAMED_MANAGERS = []
HRP_NAMED_MANAGERS = LDP_LONG_MANAGERS + HRP_LS_NAMED_MANAGERS