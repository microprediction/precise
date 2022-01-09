import numpy as np

# Minor adaptations to code by Carsten Schelp
# https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html


class OnlineEmpiricalCovariance:
    """
    A class to calculate the mean and the covariance matrix
    of the incrementally added, n-dimensional data.
    """

    def __init__(self, order):
        """
        Parameters
        ----------
        order: int, The order (=="number of features") of the incrementally added
        dataset and of the resulting covariance matrix.
        """
        self._order = order
        self._shape = (order, order)
        self._identity = np.identity(order)
        self._ones = np.ones(order)
        self._count = 0
        self._mean = np.zeros(order)
        self._cov = np.zeros(self._shape)

    @property
    def count(self):
        """
        int, The number of observations that has been added
        to this instance of OnlineCovariance.
        """
        return self._count

    @property
    def mean(self):
        """
        double, The mean of the added data.
        """
        return self._mean

    @property
    def cov(self):
        """
        array_like, The covariance matrix of the added data.
        """
        return self._cov

    @property
    def corrcoef(self):
        """
        array_like, The normalized covariance matrix of the added data.
        Consists of the Pearson Correlation Coefficients of the data's features.
        """
        if self._count < 1:
            return None
        variances = np.diagonal(self._cov)
        denominator = np.sqrt(variances[np.newaxis, :] * variances[:, np.newaxis])
        return self._cov / denominator

    def add(self, observation):
        """
        Add the given observation to this object.

        Parameters
        ----------
        observation: array_like, The observation to add.
        """
        if self._order != len(observation):
            raise ValueError(f'Observation to add must be of size {self._order}')

        self._count += 1
        delta_at_nMin1 = np.array(observation - self._mean)
        self._mean += delta_at_nMin1 / self._count
        weighted_delta_at_n = np.array(observation - self._mean) / self._count
        D_at_n = np.broadcast_to(weighted_delta_at_n, self._shape).T
        D = (delta_at_nMin1 * self._identity).dot(D_at_n.T)
        self._cov = self._cov * (self._count - 1) / self._count + D

    def merge(self, other):
        """
        Merges the current object and the given other object into a new OnlineCovariance object.

        Parameters
        ----------
        other: OnlineCovariance, The other OnlineCovariance to merge this object with.

        Returns
        -------
        OnlineEmpiricalCovariance
        """
        if other._order != self._order:
            raise ValueError(
                f'''
                   Cannot merge two OnlineCovariances with different orders.
                   ({self._order} != {other._order})
                   ''')

        merged_cov = OnlineEmpiricalCovariance(self._order)
        merged_cov._count = self.count + other.count
        count_corr = (other.count * self.count) / merged_cov._count
        merged_cov._mean = (self.mean / other.count + other.mean / self.count) * count_corr
        flat_mean_diff = self._mean - other._mean
        mean_diffs = np.broadcast_to(flat_mean_diff, self._shape).T
        merged_cov._cov = (self._cov * self.count \
                           + other._cov * other._count \
                           + mean_diffs * mean_diffs.T * count_corr) \
                          / merged_cov.count
        return merged_cov