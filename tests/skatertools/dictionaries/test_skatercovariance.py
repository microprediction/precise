import pytest
import numpy as np
from precise.skatertools.dictionaries.skatercovariance import SkaterCovariance
from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r01

@pytest.fixture
def skater_cov():
    """Fixture to initialize SkaterCovariance."""
    return SkaterCovariance(min_longevity_for_clone=2)

def example_data_stream():
    """Generate a simulated data stream."""
    return [
        # Universe 1: Keys A-F
        {'A': np.random.randn(), 'B': np.random.randn(), 'C': np.random.randn(),
         'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn()},
        # Universe 2: Keys B-G (A leaves, G enters)
        {'B': np.random.randn(), 'C': np.random.randn(), 'D': np.random.randn(),
         'E': np.random.randn(), 'F': np.random.randn(), 'G': np.random.randn()},
        # Universe 3: Keys C-H (B leaves, H enters)
        {'C': np.random.randn(), 'D': np.random.randn(), 'E': np.random.randn(),
         'F': np.random.randn(), 'G': np.random.randn(), 'H': np.random.randn()},
        # Universe 4: Keys D-I (C leaves, I enters)
        {'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn(),
         'G': np.random.randn(), 'H': np.random.randn(), 'I': np.random.randn()},
    ] * 5  # Repeat for multiple updates

@pytest.mark.parametrize("k", [1])
def test_skater_covariance(skater_cov, k):
    """Test SkaterCovariance updates and correlation matrix retrieval."""
    data_stream = example_data_stream()

    def f(y, s, k=k):
        return ewa_emp_pcov_d0_r01(y=y, s=s, k=k)

    # First update lap
    for x in data_stream:
        skater_cov.update(x=x, f=f)

    # Second update lap and correlation matrix retrieval
    for x in data_stream:
        skater_cov.update(x=x, f=f)
        corr_matrix = skater_cov.get_corr()

        # Assert correlation matrix is not None and is square
        assert corr_matrix is not None, "Correlation matrix is None"
        assert corr_matrix.shape[0] == corr_matrix.shape[1], "Correlation matrix is not square"
