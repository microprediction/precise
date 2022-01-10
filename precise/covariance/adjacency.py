import numpy as np
import math
from precise.covariance.util import multiply_diag
from kmeans1d import cluster

def infer_adjacency(pre):
    a = np.copy(pre)
    n = np.shape(pre)[0]
    m = int(math.ceil(math.sqrt(n)))

    off_diag_values = sorted( np.abs(multiply_diag(a,lmbd=0, make_copy=True).ravel()) )
    clusters, centroids = cluster(array=off_diag_values, k=2)
    assert clusters[1]>=clusters[0]
    cutoff_value = centroids[1]/2.0

    abs_pre = np.abs(pre)

    for i in range(n):
        a[:,i] = np.vectorize(int)(abs_pre[:,i] > cutoff_value)
    for i in range(n):
        a[i,i]=1
    return a.astype(bool)





