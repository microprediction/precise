# Using the online managers estimators

1. Choose a covariance "skater" from the [listing of managers](https://github.com/microprediction/precise/blob/main/LISTING_OF_MANAGERS.md)
2. Import it
3. Pass it one data vector, or list at a time

### Example usage
Here y is a vector:

        from precise.skaters.managers.schurmanagers import schur_weak_pm_t0_d0_r025_n50_g100_long_manager as mgr
        s = {}
        for y in ys:
            w, s = mgr(s=s, y=y)
  
-+-

Documentation [home](https://microprediction.github.io/precise)


View as [source](https://github.com/microprediction/precise/blob/master/docs/managers.md) or [web](https://microprediction.github.io/precise/managers)
