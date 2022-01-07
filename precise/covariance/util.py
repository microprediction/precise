import numpy as np


def cov_to_corrcoef(cov):
    variances = np.diagonal(cov)
    denominator = np.sqrt(variances[np.newaxis, :] * variances[:, np.newaxis])
    return cov / denominator
