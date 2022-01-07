import numpy as np


def cov_to_corrcoef(cov):
    variances = np.diagonal(cov)
    denominator = np.sqrt(variances[np.newaxis, :] * variances[:, np.newaxis])
    return cov / denominator


def create_correlated_dataset(n, mu, dependency, scale):
    latent = np.random.randn(n, dependency.shape[0])
    dependent = latent.dot(dependency)
    scaled = dependent * scale
    scaled_with_offset = scaled + mu
    return scaled_with_offset