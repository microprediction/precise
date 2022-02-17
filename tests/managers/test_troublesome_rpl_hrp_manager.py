from precise.skaters.managerutil.managertesting import manager_test_run


def test_troublesome_manager(return_w=False):
    from precise.skaters.managers.rflmanagers import rfl_hrp_slpm_long_manager_n200 as mgr
    w = manager_test_run(mgr=mgr)
    if return_w:
        return w


if __name__=='__main__':
    w = test_troublesome_manager(return_w=True)
    print(w)