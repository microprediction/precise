from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r05, ewa_emp_pcov_d0_r01, ewa_emp_pcov_d0_r02
from precise.skaters.portfoliostatic.rpport import rp_port_p0, rp_port_p20, rp_port_p40, rp_port_p60, rp_port_p80
from precise.skaters.managers.covmanagerfactory import static_cov_manager_factory_d0


# Some risk parity managers powered by the excellent riskparityportfolio package


def rp_ewa_r01_p0_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r01, port=rp_port_p0, e=e,j=j,q=q)


def rp_ewa_r02_p0_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r02, port=rp_port_p0, e=e,j=j,q=q)


def rp_ewa_r05_p0_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r05, port=rp_port_p0, e=e,j=j,q=q)


def rp_ewa_r01_p20_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r01, port=rp_port_p20, e=e,j=j,q=q)


def rp_ewa_r02_p20_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r02, port=rp_port_p20, e=e,j=j,q=q)


def rp_ewa_r05_p20_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r05, port=rp_port_p20, e=e,j=j,q=q)


def rp_ewa_r01_p40_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r01, port=rp_port_p40, e=e,j=j,q=q)


def rp_ewa_r02_p40_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r02, port=rp_port_p40, e=e,j=j,q=q)


def rp_ewa_r05_p40_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r05, port=rp_port_p40, e=e,j=j,q=q)


def rp_ewa_r01_p60_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r01, port=rp_port_p60, e=e,j=j,q=q)


def rp_ewa_r02_p60_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r02, port=rp_port_p60, e=e,j=j,q=q)


def rp_ewa_r05_p60_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r05, port=rp_port_p60, e=e,j=j,q=q)


def rp_ewa_r01_p80_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r01, port=rp_port_p80, e=e,j=j,q=q)


def rp_ewa_r02_p80_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r02, port=rp_port_p80, e=e,j=j,q=q)


def rp_ewa_r05_p80_long_manager(y, s, k=1,e=1,j=1,q=1.0):
    return static_cov_manager_factory_d0(y=y, s=s, f=ewa_emp_pcov_d0_r05, port=rp_port_p80, e=e,j=j,q=q)


RP_EWA_LONG_MANAGERS = [rp_ewa_r01_p0_long_manager, rp_ewa_r02_p0_long_manager,rp_ewa_r05_p0_long_manager,
                        rp_ewa_r01_p20_long_manager, rp_ewa_r02_p20_long_manager,rp_ewa_r05_p20_long_manager,
                        rp_ewa_r01_p40_long_manager, rp_ewa_r02_p40_long_manager, rp_ewa_r05_p40_long_manager,
                        rp_ewa_r01_p60_long_manager, rp_ewa_r02_p60_long_manager, rp_ewa_r05_p60_long_manager,
                        rp_ewa_r01_p80_long_manager, rp_ewa_r02_p80_long_manager, rp_ewa_r05_p80_long_manager]


RP_LONG_MANAGERS = RP_EWA_LONG_MANAGERS  # For now. Should add some _pm_'s