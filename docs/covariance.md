
# Using the online covariance estimators

1. Choose a covariance "skater" from the [listing of cov skaters](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md)
2. Import it
3. Pass it one data vector or list at a time

### Example usage

    from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r005_n100 as f 
    s = {}
    for y in ys:
        x, x_cov, s = f(s=s, y=y)


-+-

Documentation [home](https://microprediction.github.io/precise)
