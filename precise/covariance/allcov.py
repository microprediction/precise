from precise.covariance.empirical import _emp_pcov_init, _emp_pcov_update

# List of fully autonomous estimators

COV_ESTIMATORS = {'emp':(_emp_pcov_init, _emp_pcov_update)}