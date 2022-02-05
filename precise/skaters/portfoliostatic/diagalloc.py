from precise.skaters.portfoliostatic.diagallocfactory import diagonal_allocation_factory


def diag_alloc(covs=None, pres=None):
    return diagonal_allocation_factory(covs=covs, pres=pres)


DIAG_ALLOC = [ diag_alloc ]