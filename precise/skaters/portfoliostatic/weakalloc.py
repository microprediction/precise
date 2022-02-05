from typing import List
from precise.skaters.portfoliostatic.weakallocfactory import weak_allocation_factory

# List of allocators that use cov weakening


def weak_long_alloc(covs:List, pres:List=None)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    return weak_allocation_factory(covs=covs, pres=pres)


WEAK_ALLOC = [weak_long_alloc]