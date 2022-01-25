import numpy as np
from precise.skaters.covarianceutil.covfunctions import multiply_diag
from kmeans1d import cluster


def centroid_precision_adjacency(pre:np.ndarray)->np.ndarray:
    """ Uses clustering of absolute values to infer precision adjacency matrix

    :param  pre: 2d array of precision estimates
    :return: 2d array of boolean

    """
    # A rather speculative approach, this using 1-dim version of k-means clustering to establish a
    # minimum absolute precision value. Any entry above this threshold is considered 'real'.
    a = np.copy(pre)
    n = np.shape(pre)[0]
    off_diag_values = sorted(np.abs(multiply_diag(a, phi=0, copy=True).ravel()))
    clusters, centroids = cluster(array=off_diag_values, k=3)
    assert clusters[1]>=clusters[0]
    cutoff_value = min( centroids[1]*2.0, centroids[2]/2.0 )
    abs_pre = np.abs(pre)
    for i in range(n):
        a[:,i] = np.vectorize(int)(abs_pre[:,i] > cutoff_value)
    for i in range(n):
        a[i,i]=1
    return a.astype(bool)





