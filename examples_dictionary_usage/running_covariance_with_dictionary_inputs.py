# Example skater function following the precise package conventions
from precise.skatertools.dictionaries.skatercovariance import SkaterCovariance
import numpy as np

if __name__ == '__main__':
    from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r01

    def f(y, s, k=1):
        return ewa_emp_pcov_d0_r01(y=y, s=s, k=k)

    # Initialize SkaterCovariance with the example skater
    skater_cov = SkaterCovariance(min_longevity_for_clone=2)

    # Simulated data updates (larger and with more keys)
    data_stream = [
        # Universe 1: Keys A-F
        {'A': np.random.randn(), 'B': np.random.randn(), 'C': np.random.randn(),
         'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn()},
        {'A': np.random.randn(), 'B': np.random.randn(), 'C': np.random.randn(),
         'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn()},
        {'A': np.random.randn(), 'B': np.random.randn(), 'C': np.random.randn(),
         'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn()},
        {'A': np.random.randn(), 'B': np.random.randn(), 'C': np.random.randn(),
         'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn()},
        {'A': np.random.randn(), 'B': np.random.randn(), 'C': np.random.randn(),
         'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn()},
        # Universe 2: Keys B-G (A leaves, G enters)
        {'B': np.random.randn(), 'C': np.random.randn(), 'D': np.random.randn(),
         'E': np.random.randn(), 'F': np.random.randn(), 'G': np.random.randn()},
        {'B': np.random.randn(), 'C': np.random.randn(), 'D': np.random.randn(),
         'E': np.random.randn(), 'F': np.random.randn(), 'G': np.random.randn()},
        {'B': np.random.randn(), 'C': np.random.randn(), 'D': np.random.randn(),
         'E': np.random.randn(), 'F': np.random.randn(), 'G': np.random.randn()},
        {'B': np.random.randn(), 'C': np.random.randn(), 'D': np.random.randn(),
         'E': np.random.randn(), 'F': np.random.randn(), 'G': np.random.randn()},
        {'B': np.random.randn(), 'C': np.random.randn(), 'D': np.random.randn(),
         'E': np.random.randn(), 'F': np.random.randn(), 'G': np.random.randn()},
        # Universe 3: Keys C-H (B leaves, H enters)
        {'C': np.random.randn(), 'D': np.random.randn(), 'E': np.random.randn(),
         'F': np.random.randn(), 'G': np.random.randn(), 'H': np.random.randn()},
        {'C': np.random.randn(), 'D': np.random.randn(), 'E': np.random.randn(),
         'F': np.random.randn(), 'G': np.random.randn(), 'H': np.random.randn()},
        {'C': np.random.randn(), 'D': np.random.randn(), 'E': np.random.randn(),
         'F': np.random.randn(), 'G': np.random.randn(), 'H': np.random.randn()},
        {'C': np.random.randn(), 'D': np.random.randn(), 'E': np.random.randn(),
         'F': np.random.randn(), 'G': np.random.randn(), 'H': np.random.randn()},
        {'C': np.random.randn(), 'D': np.random.randn(), 'E': np.random.randn(),
         'F': np.random.randn(), 'G': np.random.randn(), 'H': np.random.randn()},
        # Universe 4: Keys D-I (C leaves, I enters)
        {'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn(),
         'G': np.random.randn(), 'H': np.random.randn(), 'I': np.random.randn()},
        {'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn(),
         'G': np.random.randn(), 'H': np.random.randn(), 'I': np.random.randn()},
        {'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn(),
         'G': np.random.randn(), 'H': np.random.randn(), 'I': np.random.randn()},
        {'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn(),
         'G': np.random.randn(), 'H': np.random.randn(), 'I': np.random.randn()},
        {'D': np.random.randn(), 'E': np.random.randn(), 'F': np.random.randn(),
         'G': np.random.randn(), 'H': np.random.randn(), 'I': np.random.randn()},
    ]
    # Update with data points
    for x in data_stream:
        print({'x':x})
        skater_cov.update(x=x, f=f)

    # Second lap
    for x in data_stream:
        print({'x': x})
        skater_cov.update(x=x,f=f)

        # Retrieve correlation matrix
        corr_matrix = skater_cov.get_corr()
        print("\nCorrelation Matrix:")
        print(corr_matrix)
