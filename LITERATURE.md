


### Numerically Stable Parallel Computation of (Co-)Variance [pdf](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf)
With the advent of big data, we see an increasing interest in computing correlations in huge data sets with both many instances and
many variables. Essential descriptive statistics such as the variance,
standard deviation, covariance, and correlation can suffer from a
numerical instability known as “catastrophic cancellation” that can
lead to problems when naively computing these statistics with a
popular textbook equation. While this instability has been discussed
in the literature already 50 years ago, we found that even today,
some high-profile tools still employ the instable version.
In this paper, we study a popular incremental technique originally proposed by Welford, which we extend to weighted covariance
and correlation. We also discuss strategies for further improving
numerical precision, how to compute such statistics online on a
data stream, with exponential aging, with missing data, and a batch
parallelization for both high performance and numerical precision.
We demonstrate when the numerical instability arises, and the
performance of different approaches under these conditions. We
showcase applications from the classic computation of variance
as well as advanced applications such as stock market analysis
with exponentially weighted moving models and Gaussian mixture
modeling for cluster analysis that all benefit from this approach


- http://www.ledoit.net/ole1a.pdf
-  
