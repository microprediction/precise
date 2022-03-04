from precise.skaters.managers.schurmanagerfactory import schur_vol_vol_ewa_manager_factory,schur_diag_diag_buf_emp_manager_factory


# A Modified Hierarchical Risk Parity Framework for Portfolio Management
# Inspired by Marat Molyboga
# https://jfds.pm-research.com/content/early/2020/07/03/jfds.2020.1.038


def molyboga_r025_n50_long_manager(y, s, k=1, e=1):
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, r=0.025, n_emp=40, e=e, gamma=0, delta=0)


def molyboga_r001_n100_long_manger(y, s, k=1, e=1):
    return schur_vol_vol_ewa_manager_factory(y=y, s=s, r=0.01, n_emp=100, e=e, gamma=0, delta=0)


MOLYBOGA_LONG_MANAGERS = [molyboga_r025_n50_long_manager,
                          molyboga_r001_n100_long_manger
                          ]