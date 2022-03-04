from precise.skaters.portfoliostatic.volallocfactory import vol_allocation_factory


def vol_alloc(covs=None, pres=None):
    return vol_allocation_factory(covs=covs, pres=pres)


VOL_ALLOC = [ vol_alloc ]