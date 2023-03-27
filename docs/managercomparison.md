# Comparing managers 



### Empirical comparison 
Using [manager_stats_leaderboard](https://github.com/microprediction/precise/blob/main/precise/skatervaluation/managercomparisonutil/managerstats.py):

    xs =    # ... one column per variable
    mrgs =  # ... list of managers 
    j = 1   # How often to rebalance
    q = 1.0 # How far to move towards target when rebalancing
    lb = manager_stats_leaderboard(mgrs=mrgs, xs=xs, verbose=True, field='info', j=j, q=q)


See [metals_schur_manager_comparison](https://github.com/microprediction/precise/blob/main/examples_managers/metals/metals_schur_manager_comparison.py)


-+-

Documentation [home](https://microprediction.github.io/precise)


View as [source](https://github.com/microprediction/precise/blob/master/docs/managercomparison.md) or [web](https://microprediction.github.io/precise/managercomparison)
