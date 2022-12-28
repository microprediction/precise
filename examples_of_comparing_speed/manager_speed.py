from pprint import pprint
from precise.skaters.managers.schurmanagers import schur_weak_weak_pm_t0_r025_n50_s25_g100_h125_long_manager as mgr
from precise.skatervaluation.managercomparisonutil.managertesting import manager_profile

if __name__=='__main__':
    cpu = manager_profile(mgr=mgr)
    pprint(cpu)