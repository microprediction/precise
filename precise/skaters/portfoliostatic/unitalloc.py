from precise.skaters.portfoliostatic.unitallocfactory import unitary_min_var_allocation_factory


def a_unit(covs=None, pres=None):
    return unitary_min_var_allocation_factory(covs=covs,pres=pres)


UNIT_ALLOC = [ a_unit ]