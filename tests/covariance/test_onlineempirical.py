
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.covariance.onlineempirical import online_empirical_cov,merge_online_empirical_cov
from precise.covariance.util import create_correlated_dataset


def test_onlineempirical():
    data = create_correlated_dataset(10000, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    conventional_mean = np.mean(data, axis=0)
    conventional_cov = np.cov(data, rowvar=False)
    conventional_corrcoef = np.corrcoef(data, rowvar=False)
    ocov = online_empirical_cov(n_dim=data.shape[1])
    for observation in data:
        ocov = online_empirical_cov(s=ocov, y=observation)
    assert np.isclose(conventional_mean, ocov['mean']).all(), \
        """
        Mean should be the same with both approaches.
        """
    assert np.isclose(conventional_cov, ocov['cov'], atol=1e-3).all(), \
        """
        Covariance-matrix should be the same with both approaches.
        """
    from precise.covariance.util import cov_to_corrcoef
    ocorr = cov_to_corrcoef(ocov['cov'])
    assert np.isclose(conventional_corrcoef, ocorr).all(), \
        """
        Pearson-Correlationcoefficient-matrix should be the same with both approaches.
        """


def test_merging():
    data_part1 = create_correlated_dataset(500, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    data_part2 = create_correlated_dataset( \
        1000, (5, 6, 2), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    ocov_part1 = online_empirical_cov(n_dim=3)
    ocov_part2 = online_empirical_cov(n_dim=3)
    ocov_both = online_empirical_cov(n_dim=3)

    # "grow" online-covariances for part 1 and 2 separately but also
    # put all observations into the OnlineCovariance object for both.

    for row in data_part1:
        ocov_part1 = online_empirical_cov(s=ocov_part1, y=row)
        ocov_both = online_empirical_cov(s=ocov_both, y=row)

    for row in data_part2:
        ocov_part2 = online_empirical_cov(s=ocov_part2, y=row)
        ocov_both = online_empirical_cov(s=ocov_both, y=row)

    ocov_merged = merge_online_empirical_cov(s=ocov_part1, other_s=ocov_part2)
    assert ocov_both['count'] == ocov_merged['count']
    assert np.isclose(ocov_both['mean'], ocov_merged['mean']).all()
    assert np.isclose(ocov_both['cov'], ocov_merged['cov']).all()


if __name__=='__main__':
    test_onlineempirical()
    test_merging()