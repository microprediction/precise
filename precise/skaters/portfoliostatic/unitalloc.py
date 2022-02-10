from precise.skaters.portfoliostatic.unitallocfactory import unitary_min_var_allocation_factory


def unit_alloc(covs=None, pres=None):
    return unitary_min_var_allocation_factory(covs=covs,pres=pres)


UNIT_ALLOC = [unit_alloc]