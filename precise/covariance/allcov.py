from precise.covariance.empirical import ecov_init, ecov_update

# List of fully autonomous estimators

COV_ESTIMATORS = {'emp':(ecov_init,ecov_update)}