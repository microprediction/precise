from precise.skaters.managers.schurmanagerfactory import schur_diag_diag_buf_emp_manager_factory
   # Note: Could also consider more based on schur_vol_vol_ewa_manager_factory

# Stands for Lopez de Prado
# Some Hierarchical Risk-Parity managers very loosely based on some literature
# (Note that seriation may be different so this is not supposed to be a replica)


def ldp_s2_n50_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=50, e=e, gamma=0, delta=0, j=j, q=q, n_split=2)


def ldp_s5_n50_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=50, e=e, gamma=0, delta=0, j=j, q=q, n_split=5)


def ldp_s25_n50_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=50, e=e, gamma=0, delta=0, j=j, q=q, n_split=25)


def ldp_s5_n100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0, j=j, q=q, n_split=5)


def ldp_s25_n100_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0, j=j, q=q, n_split=25)


# Conv hull managers 

def ldp_s2_n200_l5_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0, j=j, q=q, l=5, n_split=2)


def ldp_s5_n200_l5_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0, j=j, q=q, l=5, n_split=5)


def ldp_s5_n200_l21_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0, j=j, q=q, l=21, n_split=5)


def ldp_s100_n200_l21_long_manager(y, s, k=1, e=1, j=1, q=1.0):
    assert k == 1
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0, j=j, q=q, l=21, n_split=100)




LDP_LONG_MANAGERS = [ldp_s2_n50_long_manager, ldp_s5_n50_long_manager, ldp_s25_n50_long_manager,
                     ldp_s5_n100_long_manager, ldp_s25_n100_long_manager,
                     ldp_s5_n200_l5_long_manager, ldp_s5_n200_l21_long_manager,
                     ldp_s100_n200_l21_long_manager, ldp_s2_n200_l5_long_manager]
HRP_LS_NAMED_MANAGERS = []
HRP_NAMED_MANAGERS = LDP_LONG_MANAGERS + HRP_LS_NAMED_MANAGERS
