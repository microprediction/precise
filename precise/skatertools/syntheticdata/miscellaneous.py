import numpy as np
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




