


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


### A Well-Conditioned Estimator For Large-Dimensional Covariance Matrices [pdf](http://www.ledoit.net/ole1a.pdf) 
Ledoit and Wolf

Many applied problems require a covariance matrix estimator that is not only invertible,
but also well-conditioned (that is, inverting it does not amplify estimation error). For largedimensional covariance matrices, the usual estimator—the sample covariance matrix—is
typically not well-conditioned and may not even be invertible. This paper introduces
an estimator that is both well-conditioned and more accurate than the sample covariance
matrix asymptotically. This estimator is distribution-free and has a simple explicit formula
that is easy to compute and interpret. It is the asymptotically optimal convex linear
combination of the sample covariance matrix with the identity matrix. Optimality is meant
with respect to a quadratic loss function, asymptotically as the number of observations and
the number of variables go to infinity together. Extensive Monte-Carlo confirm that the
asymptotic results tend to hold well in finite sample.


### A Robust Estimator of the Efficient Frontier [pdf](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3498628_code434076.pdf?abstractid=3469961&mirid=1&type=2)
Marcos Lopez de Prado

Convex optimization solutions tend to be unstable, to the point of entirely offsetting the benefits of optimization. For example, in the context of financial applications, it is known that portfolios optimized in-sample often underperform the naïve (equal weights) allocation out-of-sample. This instability can be traced back to two sources: (i) noise in the input variables; and (ii) signal structure that magnifies the estimation errors in the input variables. A first innovation of this paper is to introduce the nested clustered optimization algorithm (NCO), a method that tackles both sources of instability.


### Noisy Covariance Matrices and Portfolio Optimization [pdf](https://arxiv.org/pdf/cond-mat/0111503.pdf)
According to recent findings [1, 2], empirical covariance matrices deduced from
financial return series contain such a high amount of noise that, apart from a
few large eigenvalues and the corresponding eigenvectors, their structure can
essentially be regarded as random. In [1], e.g., it is reported that about 94%
of the spectrum of these matrices can be fitted by that of a random matrix
drawn from an appropriately chosen ensemble. In view of the fundamental
role of covariance matrices in the theory of portfolio optimization as well as in
industry-wide risk management practices, we analyze the possible implications
of this effect.

### Shrinkage Algorithms for MMSE Covariance Estimation [pdf](https://webee.technion.ac.il/Sites/People/YoninaEldar/104.pdf)
Chen, Wiesel, Eldar, Hero

Abstract—We address covariance estimation in the sense of
minimum mean-squared error (MMSE) when the samples are
Gaussian distributed. Specifically, we consider shrinkage methods
which are suitable for high dimensional problems with a small
number of samples (large  small ). First, we improve on the
Ledoit-Wolf (LW) method by conditioning on a sufficient statistic.
By the Rao-Blackwell theorem, this yields a new estimator called
RBLW, whose mean-squared error dominates that of LW for
Gaussian variables

### PORTFOLIO OPTIMIZATION WITH NOISY COVARIANCE MATRICES [pdf](https://www.joim.com/wp-content/uploads/emember/downloads/p0594.pdf)
Menchero and Ji 2019 

In this paper, we explore the effect of sampling error in the asset covariance matrix when
constructing portfolios using mean–variance optimization. We show that as the covariance
matrix becomes increasingly ill-conditioned (i.e., “noisy”), optimized portfolios exhibit
certain undesirable characteristics such as under-prediction of risk, increased out-ofsample volatility, inefficient risk allocation, and increased leverage and turnover. We explain these results by utilizing the concept of alpha portfolios (which explain expected
returns) and hedge portfolios (which serve to reduce risk). We show that noise in the
covariance matrix leads to systematic biases in the volatility and correlation forecasts of
these portfolios, which in turn explains the adverse effects cited above


### NONLINEAR SHRINKAGE ESTIMATION OF LARGE-DIMENSIONAL COVARIANCE MATRICES [pdf](https://arxiv.org/pdf/1207.5322.pdf)
Ledoit and Wolf

Many statistical applications require an estimate of a covariance
matrix and/or its inverse. When the matrix dimension is large compared to the sample size, which happens frequently, the sample covariance matrix is known to perform poorly and may suffer from
ill-conditioning. There already exists an extensive literature concerning improved estimators in such situations. In the absence of further knowledge about the structure of the true covariance matrix,
the most successful approach so far, arguably, has been shrinkage
estimation. Shrinking the sample covariance matrix to a multiple of
the identity, by taking a weighted average of the two, turns out to
be equivalent to linearly shrinking the sample eigenvalues to their
grand mean, while retaining the sample eigenvectors. Our paper extends this approach by considering nonlinear transformations of the
sample eigenvalues. We show how to construct an estimator that is
asymptotically equivalent to an oracle estimator suggested in previous work. As demonstrated in extensive Monte Carlo simulations,
the resulting bona fide estimator can result in sizeable improvements
over the sample covariance matrix and also over linear shrinkage.

### Covariance versus Precision Matrix Estimation for Efficient Asset Allocation [pdf](https://www.afg.asso.fr/wp-content/uploads/2016/02/Covariance_versus_Precision_Matrix_Estimation_Efficient_Asset_Allocation.pdf)

Senneret, Malevergne, Abry, Perrin, Jafffres

Asset allocation constitutes one of the most crucial
and most challenging task in financial engineering. In many
allocation strategies, the estimation of large covariance or precision matrices from short time span multivariate observations
is a mandatory yet difficult step. In the present contribution,
a large selection of elementary to advanced estimation procedures for the covariance as well as for precision matrices,
are organized into classes of estimation principles, reviewed
and compared. To complement this overview, several additional
estimators are explicitly derived and studied theoretically. Rather
than estimation performance evaluated from synthetic simulated
data, performance of the estimation procedures are assessed
empirically by financial criteria (volatility, Sharpe ratio,. . . )
quantifying the quality of asset allocation in the mean-variance
framework. Performance are quantified by application to a large
set of about 250 European stock returns across the last 15 years,
up to August 2015

### Noise Dressing of Financial Correlation Matrices [pdf](https://arxiv.org/pdf/cond-mat/9810255.pdf)
Laloux, Cizeau, Bouchaud, Potters 2008

We show that results from the theory of random matrices are potentially of great interest to
understand the statistical structure of the empirical correlation matrices appearing in the study of
price fluctuations. The central result of the present study is the remarkable agreement between the
theoretical prediction (based on the assumption that the correlation matrix is random) and empirical
data concerning the density of eigenvalues associated to the time series of the different stocks of the
S&P500 (or other major markets). In particular the present study raises serious doubts on the blind
use of empirical correlation matrices for risk management.

### Tuning the Parameters for Precision Matrix Estimation Using Regression Analysis [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8755295)
Tong, Yang, Zi, Yu and Ogunbona 2019

Precision matrix, i.e., inverse covariance matrix, is widely used in signal processing, and often
estimated from training samples. Regularization techniques, such as banding and rank reduction, can be
applied to the covariance matrix or precision matrix estimation for improving the estimation accuracy when
the training samples are limited. In this paper, exploiting regression interpretations of the precision matrix,
we introduce two data-driven, distribution-free methods to tune the parameter for regularized precision
matrix estimation. The numerical examples are provided to demonstrate the effectiveness of the proposed
methods and example applications in the design of minimum mean squared error (MMSE) channel estimators
for large-scale multiple-input multiple-output (MIMO) communication systems are demonstrated.

### An Overview on the Estimation of Large Covariance and Precision Matrices [pdf](https://arxiv.org/pdf/1504.02995.pdf)
Fan, Liao and Liu 2015

Estimating large covariance and precision matrices are fundamental in modern multivariate analysis. The problems arise from statistical analysis of large panel economics
and finance data. The covariance matrix reveals marginal correlations between variables, while the precision matrix encodes conditional correlations between pairs of
variables given the remaining variables. In this paper, we provide a selective review of
several recent developments on estimating large covariance and precision matrices. We
focus on two general approaches: rank based method and factor model based method.
Theories and applications of both approaches are presented. These methods are expected to be widely applicable to analysis of economic and financial data.

### Unbiased Estimation of the Reciprocal Mean for Non-negative Random Variables
MOka, Kroese, Juneja 2019

Many simulation problems require the estimation of a ratio of two expectations. In recent
years Monte Carlo estimators have been proposed that can estimate such ratios without bias.
We investigate the theoretical properties of such estimators for the estimation of β = 1/EZ,
where Z ≥ 0. The estimator, βb(w), is of the form w/fw(N)
QN
i=1(1 − w Zi), where w < 2β and
N is any random variable with probability mass function fw on the positive integers. For a
fixed w, the optimal choice for fw is well understood, but less so the choice of w. We study
the properties of βb(w) as a function of w and show that its expected time variance product decreases as w decreases, even though the cost of constructing the estimator increases with w. We
also show that the estimator is asymptotically equivalent to the maximum likelihood (biased)
ratio estimator and establish practical confidence intervals.

### Distributionally Robust Inverse Covariance Estimation: The Wasserstein Shrinkage Estimator [pdf](https://arxiv.org/pdf/1805.07194.pdf)
Nguyen, Kuhn, Esfahani 2018

We introduce a distributionally robust maximum likelihood estimation model with a Wasserstein
ambiguity set to infer the inverse covariance matrix of a p-dimensional Gaussian random vector from n independent samples. The proposed model minimizes the worst case (maximum) of Stein’s loss across all normal
reference distributions within a prescribed Wasserstein distance from the normal distribution characterized
by the sample mean and the sample covariance matrix. We prove that this estimation problem is equivalent
to a semidefinite program that is tractable in theory but beyond the reach of general purpose solvers for
practically relevant problem dimensions p. In the absence of any prior structural information, the estimation
problem has an analytical solution that is naturally interpreted as a nonlinear shrinkage estimator.

### The Distance Precision Matrix: computing networks from non-linear relationships [via](https://academic.oup.com/bioinformatics/article/35/6/1009/5079333)
Ghanbari, Lasserre, Vingron 2019

We propose Distance Precision Matrix, a network reconstruction method aimed at both linear and non-linear data. Like partial distance correlation, it builds on distance covariance, a measure of possibly non-linear association, and on the idea of full-order partial correlation, which allows to discard indirect associations. We provide evidence that the Distance Precision Matrix method can successfully compute networks from linear and non-linear data, and consistently so across different datasets, even if sample size is low. The method is fast enough to compute networks on hundreds of nodes.

### A Comparison of Methods for Estimating the Determinant of High-Dimensional Covariance Matrix [pdf](https://www.math.hkbu.edu.hk/~tongt/papers/IJB2017.pdf)
Hu, Dong, Dai, Tong 2017 

The determinant of the covariance matrix for high-dimensional data plays an important role in
statistical inference and decision. It has many real applications including statistical tests and information
theory. Due to the statistical and computational challenges with high dimensionality, little work has been
proposed in the literature for estimating the determinant of high-dimensional covariance matrix. In this
paper, we estimate the determinant of the covariance matrix using some recent proposals for estimating
high-dimensional covariance matrix. Specifically, we consider a total of eight covariance matrix estimation
methods for comparison.

### Optimal Shrinkage Estimation of Variances With Applications to Microarray Data Analysis [via](https://www.researchgate.net/publication/4742786_Optimal_Shrinkage_Estimation_of_Variances_With_Applications_to_Microarray_Data_Analysis)
Tong, Wang 2007

In this paper we propose a family of shrinkage estimators for variances raised to a flxed power. We derive optimal shrinkage parameters under both Stein and the squared loss functions. Our results show that the standard sample variance is inadmissible under either loss functions. We propose several estimators for the optimal shrinkage parameters and investigate their asymptotic properties under two scenarios: large number of replica- tions and large number of genes.

### DYNAMIC PORTFOLIO OPTIMIZATION WITH INVERSE COVARIANCE CLUSTERING [pdf](https://arxiv.org/pdf/2112.15499.pdf)
Wang, Aste 2022

Market conditions change continuously. However, in portfolio’s investment strategies, it is hard to
account for this intrinsic non-stationarity. In this paper, we propose to address this issue by using the
Inverse Covariance Clustering (ICC) method to identify inherent market states and then integrate such
states into a dynamic portfolio optimization process. Extensive experiments across three different
markets, NASDAQ, FTSE and HS300, over a period of ten years, demonstrate the advantages of our
proposed algorithm, termed Inverse Covariance Clustering-Portfolio Optimization (ICC-PO)

### Portfolio Optimization with Sparse Multivariate Modelling [via](https://www.researchgate.net/publication/350484158_Portfolio_Optimization_with_Sparse_Multivariate_Modelling)
Procacci, Aste

Portfolio optimization approaches inevitably rely on multivariate modeling of markets and the economy. In this paper, we address three sources of error related to the modeling of these complex systems: 1. oversimplifying hypothesis; 2. uncertainties resulting from parameters' sampling error; 3. intrinsic non-stationarity of these systems. For what concerns point 1. we propose a L0-norm sparse elliptical modeling and show that sparsification is effective. The effects of points 2. and 3. are quantifified by studying the models' likelihood in- and out-of-sample for parameters estimated over train sets of different lengths. We show that models with larger off-sample likelihoods lead to better performing portfolios up to when two to three years of daily observations are included in the train set.

### Parsimonious Modelling with Information Filtering Networks
Barfuss, Massara, Matteo, Aste

We introduce a methodology to construct parsimonious probabilistic models. This method makes
use of Information Filtering Networks to produce a robust estimate of the global sparse inverse covariance from a simple sum of local inverse covariances computed on small sub-parts of the network.
Being based on local and low-dimensional inversions, this method is computationally very efficient
and statistically robust even for the estimation of inverse covariance of high-dimensional, noisy and
short time-series. Applied to financial data our method results computationally more efficient than
state-of-the-art methodologies such as Glasso producing, in a fraction of the computation time, models that can have equivalent or better performances but with a sparser inference structure. We also
discuss performances with sparse factor models where we notice that relative performances decrease
with the number of factors. 

### HIGH-DIMENSIONAL PRECISION MATRIX ESTIMATION WITH A KNOWN GRAPHICAL STRUCTURE [pdf](https://arxiv.org/pdf/2107.06815.pdf)
Le and Zhong 2021

A precision matrix is the inverse of a covariance matrix. In this paper, we study the problem of
estimating the precision matrix with a known graphical structure under high-dimensional settings.
We propose a simple estimator of the precision matrix based on the connection between the known
graphical structure and the precision matrix. We obtain the rates of convergence of the proposed
estimators and derive the asymptotic normality of the proposed estimator in the high-dimensional
setting when the data dimension grows with the sample size. Numerical simulations are conducted
to demonstrate the performance of the proposed method. We also show that the proposed method
outperforms some existing methods that do not utilize the graphical structure information

### The Graphical Lasso: New Insights and Alternatives [pdf](https://hastie.su.domains/Papers/glasso_revisit_trevor_arxiv.pdf)
Mazumder, Hastie

We show that in fact glasso is solving the dual of the graphical lasso penalized likelihood,
by block coordinate descent. In this dual, the target of estimation is Σ, the covariance matrix,
rather than the precision matrix Θ. We propose similar primal algorithms p-glasso and dpglasso, that also operate by block-coordinate descent, where Θ is the optimization target. We
study all of these algorithms, and in particular different approaches to solving their coordinate
subproblems. We conclude that dp-glasso is superior from several points of view.

### Covariance Prediction via Convex Optimization [pdf](https://stanford.edu/~boyd/papers/pdf/forecasting_covariances.pdf)
Barratt, Boyd 2021

We consider the problem of predicting the covariance of a zero mean Gaussian
vector, based on another feature vector. We describe a covariance predictor that has
the form of a generalized linear model, i.e., an affine function of the features followed
by an inverse link function that maps vectors to symmetric positive definite matrices.
The log-likelihood is a concave function of the predictor parameters, so fitting the
predictor involves convex optimization. Such predictors can be combined with others,
or recursively applied to improve performance.

### A review of two decades of correlations, hierarchies, networks and clustering in financial markets [pdf](https://arxiv.org/pdf/1703.00485.pdf)
Marti, Nielsen, Binkowski, Donnat 2020

We review the state of the art of clustering financial time series and the study of their correlations alongside
other interaction networks. The aim of this review is to gather in one place the relevant material from
different fields, e.g. machine learning, information geometry, econophysics, statistical physics, econometrics,
behavioral finance. We hope it will help researchers to use more effectively this alternative modeling of the
financial time series. Decision makers and quantitative researchers may also be able to leverage its insights.
Finally, we also hope that this review will form the basis of an open toolbox to study correlations, hierarchies,
networks and clustering in financial markets.

### An Linfinity Eigenvector Perturbation Bound and Its Application to Robust Covariance Estimation [pdf](https://www.jmlr.org/papers/volume18/16-140/16-140.pdf)
Fan, Wang, Zhong

In statistics and machine learning, we are interested in the eigenvectors (or singular vectors) of certain matrices (e.g. covariance matrices, data matrices, etc). However, those
matrices are usually perturbed by noises or statistical errors, either from random sampling
or structural patterns. The Davis-Kahan sin θ theorem is often used to bound the difference between the eigenvectors of a matrix A and those of a perturbed matrix Ae = A + E,
in terms of `2 norm. In this paper, we prove that when A is a low-rank and incoherent
matrix, the `∞ norm perturbation bound of singular vectors (or eigenvectors in the symmetric case) is smaller by a factor of √
d1 or √
d2 for left and right vectors, where d1 and d2
are the matrix dimensions. The power of this new perturbation result is shown in robust
covariance estimation, particularly when random variables have heavy tails. There, we propose new robust covariance estimators and establish their asymptotic properties using the
newly developed perturbation bound. Our theoretical results are verified through extensive
numerical experiments.
