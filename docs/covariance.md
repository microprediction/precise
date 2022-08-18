
# Using the online covariance estimators

1. Choose a covariance "skater" from the [listing of cov skaters](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md)
2. Import it
3. Pass it one data vector or list at a time

### Example usage

    from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r005_n100 as f 
    s = {}
    for y in ys:
        x, x_cov, s = f(s=s, y=y)


### Interpreting covariance skater names 
Examples:

| Skater name            | Location   | Meaning            |
|------------------------|------------|--------------------|
| buf_huber_pcov_d1_a1_b2_n50 | [skaters/covariance/bufhuber](https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/bufhuber.py) | Applies an approach that exploits Huber pseudo-means to a buffer of data of length 50 in need of differencing once, with generalized Huber loss parameters a=1, b=2. | 
| buf_sk_ld_pcov_d0_n100 | [skaters/covariance/bufsk](https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/bufsk.py) | Applies sk-learn's implementation of Ledoit-Wolf to stationary buffered data of length 100 | 
| ewa_pm_emp_scov_r01 | [skaters/covariance/ewapartial](https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/ewapartial.py) | Performs an incremental, recency-weighted sample covariance estimate that exploits partial moments. Uses a memory parameter r=0.01 | 

Broad calculation style categories

| Shorthand | Interpretation                                                                  | Incremental ? |
|-----------|---------------------------------------------------------------------------------|---------------|
| buf       | Performs classical batch calculation on a fixed window of data each time        | No            |
| win       | Performs incremental fixed window calculation.                                  | Yes           |
| run       | Running calculation weighing all observations equally                           | Yes           |  
| ewa       | Running calculation weighing recent observations more                           | Yes           |

Methodology hints (can be combined)

| Shorthand | Inspiration                            |
|-----------|----------------------------------------|
| emp       | "Empirical" (not shrunk or augmented)  |
| lz        | Le-Zhong variable-by-variable updating |
| lw        | Ledoit-Wolf                            |
| pm        | Partial moments                        | 
| huber     | Generalized Huber pseudo-mean          |
| oas       | Oracle approximating shrinkage.        |
| gl        | Graphical Lasso                        |
| mcd       | Minimum covariance determinant         |
| weak      | Novel shrinkage method by yours truly  |

Intended main target (more than one may be produced in the state)

| Shorthand | Intent                            |
|-----------|-----------------------------------|
| scov      | Sample covariance                 |
| pcov      | Population covariance             |
| spre      | Inverse of sample covariance      |
| ppre      | Inverse of population covariance  |
     
Differencing hints:

| Shorthand | Intent                                                  |
|-----------|---------------------------------------------------------|
| d0        | For use on stationary, ideally IID data                 |
| d1        | For use on data that is iid after taking one difference | 
     





-+-

Documentation [home](https://microprediction.github.io/precise)
