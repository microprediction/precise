import numpy as np
import math

def infer_adjacency(pre):
    a = np.copy(pre)
    n = np.shape(pre)[0]
    m = int(math.ceil(math.sqrt(n)))
    for i in range(n):
        xs = [abs(xi) for xi in pre[:,i]]
        theshold = sorted(xs)[m]
        a[:,i] = np.vectorize(int)(xs<theshold)
    for i in range(n):
        a[i,i]=1
    return a.astype(bool)





