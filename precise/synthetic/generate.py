import numpy as np
from sklearn.datasets import make_spd_matrix
import random


def create_correlated_dataset(n, mu=None, dependency=None, scale=None):
    if mu is None:
        mu = (2.2, 4.4, 1.5)
    if dependency is None:
        dependency = np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]])
    if scale is None:
        scale = (1, 5, 3)
    latent = np.random.randn(n, dependency.shape[0])
    dependent = latent.dot(dependency)
    scaled = dependent * scale
    x = scaled + mu
    return x


def create_factor_dataset(n, n_dim):
    Eidio = make_spd_matrix(n_dim=n_dim)
    Xidio = np.random.multivariate_normal(mean=np.zeros(n_dim), cov = Eidio, size=n)
    D = np.diag([ random.choice([0.25,1.0,4]) for _ in range(n_dim) ])
    Ecommon = 0.4*np.eye(n_dim) + 0.6*np.ones(n_dim)
    cov_common = np.matmul(np.matmul(D,Ecommon),D)
    Xcommon = np.random.multivariate_normal(mean=np.zeros(n_dim), cov = Ecommon, size=n)
    x = Xcommon + Xidio
    return x


def create_disjoint_dataset(n, n_dims:[int]):
    xs = [ create_factor_dataset(n,n_dim) for n_dim in n_dims ]
    x = xs[0]
    for xi in xs[1:]:
        x = np.concatenate( [x,xi], axis=1)
    return x


def create_band_dataset(n, n_dim, n_bands=5):
    z1 = create_factor_dataset(n,n_dim)
    z2 = create_factor_dataset(n, n_dim)
    R = np.zeros(shape=(n_dim,n_dim))
    for i in range(n_dim):
        R[i,i] = 0.75
        try:
            for j in range(1,n_bands+1):
                R[i,i+j] = np.random.rand()*0.5
        except IndexError:
            pass
    x = np.matmul(z1,R.T) + z1
    return x


