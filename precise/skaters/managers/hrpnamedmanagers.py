from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_ewa_manager_factory,schur_diag_diag_buf_emp_manager_factory


# Some Hierarchical Risk-Parity managers very loosely based on some literature


# Original Hierarchical Risk Parity approach
# (Note that seriation may be different so this is not supposed to be a replica)


def lopez_de_prado_s5_n50_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=50, e=e, gamma=0, delta=0)


def lopez_de_prado_s25_n50_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=50, e=e, gamma=0, delta=0)


def lopez_de_prado_s5_n100_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0)


def lopez_de_prado_s25_n100_long_manager(y, s, k=1, e=1):
    return schur_diag_diag_buf_emp_manager_factory(y=y, s=s, n_buffer=100, e=e, gamma=0, delta=0)



# A Modified Hierarchical Risk Parity Framework for Portfolio Management
# Inspired by Marat Molyboga
# https://jfds.pm-research.com/content/early/2020/07/03/jfds.2020.1.038


def molyboga_r025_n50_long_manager(y, s, k=1, e=1):
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, r=0.025, n_emp=40, e=e, gamma=0, delta=0)


def molyboga_r001_n100_long_manger(y, s, k=1, e=1):
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, r=0.01, n_emp=100, e=e, gamma=0, delta=0)




HRP_LONG_NAMED_MANAGERS = [lopez_de_prado_s5_n50_long_manager, lopez_de_prado_s25_n50_long_manager,
                           lopez_de_prado_s5_n100_long_manager, lopez_de_prado_s25_n100_long_manager, molyboga_r025_n50_long_manager,
                           molyboga_r001_n100_long_manger
                           ]
HRP_LS_NAMED_MANAGERS = []
HRP_NAMED_MANAGERS = HRP_LONG_NAMED_MANAGERS + HRP_LS_NAMED_MANAGERS