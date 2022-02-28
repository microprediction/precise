


### Numerically Stable Parallel Computation of (Co-)Variance [pdf](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf)
Erich Shubert and Michael Gertz

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


### Robust Estimation of High-Dimensional Mean Regression [pdf](https://arxiv.org/pdf/1410.2150.pdf)
Fan, Li, Wang

Data subject to heavy-tailed errors are commonly encountered in various scientific fields, especially in the modern era with explosion of massive data. To address this problem, procedures
based on quantile regression and Least Absolute Deviation (LAD) regression have been developed in recent years. These methods essentially estimate the conditional median (or quantile)
function. They can be very different from the conditional mean functions when distributions
are asymmetric and heteroscedastic. How can we efficiently estimate the mean regression functions in ultra-high dimensional setting with existence of only the second moment? To solve this
problem, we propose a penalized Huber loss with diverging parameter to reduce biases created
by the traditional Huber loss. 

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

### Accounting for the Epps effect: Realized covariation, cointegration and common factors. Unpublished paper: Oxford-Man (2007)
jeremy large [pdf](http://citeseer.ist.psu.edu/viewdoc/download?doi=10.1.1.371.4076&rep=rep1&type=pdf)

High-frequency realized variance approaches offer great promise for estimating asset prices ’ covariation, but encounter difficulties connected to the Epps effect. This paper models the Epps effect in a stochastic volatility setting. It adds dependent noise to a factor representation of prices. The noise both offsets covariation and describes plausible lags in information transmission. Non-synchronous trading, another recognized source of the effect, is not required. A resulting estimator of correlations and betas performs well on LSE mid-quote data, lending empirical credence to the approach. 



### Performance Improvements for Risk Balanced Portfolios
Kanstantsin Kulak

This paper focuses on the risk balanced portfolio approach. It comprises a careful consideration
of the techniques that can be used for tactical portfolio tilts in order to improve portfolio performance. The emphasis is on usability of these techniques by the majority of investors, regardless of
their asset preferences or risk appetite. After an overview of the topic, the macroeconomic regimes
model is constructed for portfolio tilts. Then a topic is switched to assets covariances and correlations - a crucial step in portfolio construction. Hidden Markov, regression and ARIMA models
are used in an attempt to predict future assets correlation values. The results are quantified and
analysed

### The Gerber statistic: a robust co-movement measure for portfolio optimization
Gerber, Markowitz, Ernst, Sargen, Miao, Javid

The purpose of this paper is to introduce the Gerber statistic, a robust co-movementmeasure for covariance matrix estimation for the purpose of portfolio construction. TheGerber statistic extends Kendall’s Tau by counting the proportion of simultaneous co-movements in series when their amplitudes exceed data-dependent thresholds. Sincethe statistic is neither affected by extremely large or extremely small movements, it isespecially well-suited for financial time series, which often exhibit extreme movementsas well as a great amount of noise. Operating within the mean-variance portfolio op-timization framework of Markowitz (1952, 1959), we consider the performance of theGerber statistic against two other commonly used methods for estimating the covari-ance matrix of stock returns: the sample covariance matrix (also called the historicalcovariance matrix) and shrinkage of the sample covariance matrix as formulated inLedoit and Wolf (2004). Using a well-diversified portfolio of nine assets over a thirtyyear time period (January 1990-December 2020), we empirically find that, for almostall scenarios considered, the Gerber statistic’s returns dominate those achieved by bothhistorical covariance and by the shrinkage method of Ledoit and Wolf (2004) 


### Cumulative Distribution Functions and UPM/LPM Analysis [pdf](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2148482)
Viole and Nawrocki

We show that the Cumulative Distribution Function (CDF) is represented by the ratio of the lower partial moment (LPM) ratio to the distribution for the interval in question. The addition of the upper partial moment (UPM) ratio enables us to create probability density functions (PDF) for any function without prior knowledge of its characteristics. We are able to replicate discrete distribution CDFs and PDFs for normal, uniform, poisson, and chi-square distributions, as well as true continuous distributions. This framework provides a new formulation for UPM/LPM portfolio analysis using co-partial moment matrices which are positive symmetrical semi-definite, aggregated to yield a positive symmetrical definite matrix.

## Filtering NOise from Correlation Matrices (Detection of Correlation Diversion, Pairs Trading, Risk Analysis Et al) [pdf](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2378911_code2184499.pdf?abstractid=2378911&mirid=1)
Alexander Izmailov and Brian Shay

Demonstration of the omnipresence of noise in financial correlation/covariance matrices revealed by means of random matrix theory, a branch of probability theory. Introduction of the Shannon entropy as a measure of noise in correlation matrices. Demonstration of substantial entropy decrease as a result of noise filtering on a few examples. A problem of paramount importance, but rarely addressed by buy-side and sell-side portfolio managers and other market practitioners, is the problem of filtering noise from correlation matrices. This noise is the inevitable consequence of the imperfection of traditional modeling assumptions, especially the representation of infinite returns time series as finite samples.


## Reliable Covariance Estimation [pdf](https://arxiv.org/pdf/2006.03311v3.pdf)
Ilya Soloveychik

Covariance or scatter matrix estimation is ubiquitous in most modern statistical and machine learning
applications. The task becomes especially challenging since most real-world datasets are essentially nonGaussian. The data is often contaminated by outliers and/or has heavy-tailed distribution causing the
sample covariance to behave very poorly and calling for robust estimation methodology. The natural
framework for the robust scatter matrix estimation is based on elliptical populations. Here, Tyler’s
estimator stands out by being distribution-free within the elliptical family and easy to compute. The
existing works thoroughly study the performance of Tyler’s estimator assuming ellipticity but without
providing any tools to verify this assumption when the covariance is unknown in advance. We address
the following open question: Given the sampled data and having no prior on the data generating process,
how to assess the quality of the scatter matrix estimator? In this work we show that this question can
be reformulated as an asymptotic uniformity test for certain sequences of exchangeable vectors on the
unit sphere. We develop a consistent and easily applicable goodness-of-fit test against all alternatives
to ellipticity when the scatter matrix is unknown. The findings are supported by numerical simulations
demonstrating the power of the suggest technique.

## Elliptical Black-Litterman portfolio optimization
Andrzej Palczewski and Jan Palczewski

We extend the Black-Litterman framework beyond normality to general elliptical distributions of investor’s views and asset returns and portfolio risk measured by CVaR. Unlike existing solutions, cf. Xiao and Valdez [Quant. Finan. 2015, 15:3, 509–519], the choice of distributions, with the first and second moment constant, has a significant effect on optimal portfolio weights in a way that cannot be achieved by appropriate reparametrisation of the classical Black-Litterman methodology. The posterior distribution, in general, is not in a parametric form and, therefore, we design efficient numerical algorithms for approximating it in order to compute optimal portfolio weights. Of independent interest are our results on equivalence of a variety of portfolio optimization problems for elliptical distributions with linear constraints in the sense that they select portfolios from the same efficient frontier. We further prove a mutual fund theorem in this broad framework


## Regularized M-estimators of scatter matrix [pdf](https://arxiv.org/pdf/1405.2528.pdf)
Esa Ollia and David Tyler

In this paper, a general class of regularized
M- estimators of scatter matrix are proposed which are suitable also
for low or insufficient sample support (small n and large
p) problems. The considered class constitutes a natural generalization of M-estimators of scatter matrix (Maronna, 1976) and are defined
as a solution to a penalized
M-estimation cost function that
depend on a pair
(α, β) of regularization parameters. We derive
general conditions for uniqueness of the solution using concept of
geodesic convexity. Since these conditions do not include Tyler’s M-estimator, necessary and sufficient conditions for uniqueness
of the penalized Tyler’s cost function are established separately.
For the regularized Tyler’s
M-estimator, we also derive a simple,
closed form and data dependent solution for choosing the
regularization parameter based on shape matrix matching in
the mean squared sense. An iterative algorithm that converges
to the solution of the regularized
M-estimating equation is
also provided.

## cvCovEst: Cross-validated covariance matrix estimator selection and evaluation in R [pdf](https://www.researchgate.net/publication/353470417_cvCovEst_Cross-validated_covariance_matrix_estimator_selection_and_evaluation_in_R/fulltext/60ff5b410c2bfa282a02e8d3/cvCovEst-Cross-validated-covariance-matrix-estimator-selection-and-evaluation-in-R.pdf?origin=figuresDialog_download)
Boileau, Hejazi, Collica, van der Laan, Dudoit

Covariance matrices play fundamental roles in myriad statistical procedures. When the observations in a dataset far outnumber the features, asymptotic theory and empirical evidence have
demonstrated the sample covariance matrix to be the optimal estimator of this parameter.
This assertion does not hold when the number of observations is commensurate with or smaller
than the number of features. Consequently, statisticians have derived many novel covariance
matrix estimators for the high-dimensional regime, often relying on additional assumptions
about the parameter’s structural characteristics (e.g., sparsity). While these estimators have
greatly improved the ability to estimate covariance matrices in high-dimensional settings, objectively selecting the best estimator from among the many possible candidates remains a
largely unaddressed challenge. The cvCovEst package addresses this methodological gap
through its implementation of a cross-validated framework for covariance matrix estimator
selection. This data-adaptive procedure’s selections are asymptotically optimal under minimal
assumptions – in fact, they are equivalent to the selections that would be made if given full
knowledge of the true data-generating processes (i.e., an oracle selector

## Large Covariance Estimation by Thresholding Principal Orthogonal Complements
Fan, Liao, Mincheva

This paper deals with the estimation of a high-dimensional covariance with a conditional sparsity structure and fast-diverging eigenvalues. By assuming sparse error covariance matrix in an approximate factor model, we allow for the presence of some cross-sectional correlation even after taking out common but unobservable factors. We introduce the Principal Orthogonal complEment Thresholding (POET) method to explore such an approximate factor structure with sparsity. The POET estimator includes the sample covariance matrix, the factor-based covariance matrix (Fan, Fan, and Lv, 2008), the thresholding estimator (Bickel and Levina, 2008) and the adaptive thresholding estimator (Cai and Liu, 2011) as specific examples. We provide mathematical insights when the factor analysis is approximately the same as the principal component analysis for high-dimensional data. The rates of convergence of the sparse residual covariance matrix and the conditional sparse covariance matrix are studied under various norms. It is shown that the impact of estimating the unknown factors vanishes as the dimensionality increases. The uniform rates of convergence for the unobserved factors and their factor loadings are derived. The asymptotic results are also verified by extensive simulation studies. Finally, a real data application on portfolio allocation is presented.


## Online Cross-Validation-Based Ensemble Learning [pdf](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5671383/pdf/nihms870890.pdf)
Benkeser, Ju, Lendle, van der Laan

Online estimators update a current estimate with a new incoming batch of data without having to revisit past data thereby providing streaming estimates that are scalable to big data. We develop flexible, ensemble-based online estimators of an infinite-dimensional target parameter, such as a regression function, in the setting where data are generated sequentially by a common conditional data distribution given summary measures of the past. This setting encompasses a wide range of time-series models and as special case, models for independent and identically distributed data. Our estimator considers a large library of candidate online estimators and uses online cross-validation to identify the algorithm with the best performance. We show that by basing estimates on the cross-validation-selected algorithm, we are asymptotically guaranteed to perform as well as the true, unknown best-performing algorithm. We provide extensions of this approach including online estimation of the optimal ensemble of candidate online estimators. We illustrate excellent performance of our methods using simulations and a real data example where we make streaming predictions of infectious disease incidence using data from a large database

## Advances in High-Dimensional Covariance Matrix Estimation [via](https://depositonce.tu-berlin.de/handle/11303/5357)
Daniel Bartz

Many applications require precise estimates of high-dimensional covariance matrices. The standard estimator is the sample covariance matrix, which is conceptually simple, fast to compute and has favorable properties in the limit of infinitely many observations. The picture changes when the dimensionality is of the same order as the number of observations. In such cases, the eigenvalues of the sample covariance matrix are highly biased, the condition number becomes large and the inversion of the matrix gets numerically unstable.

A number of alternative estimators are superior in the high-dimensional setting, which include as subcategories structured estimators, regularized estimators and spectrum correction methods. In this thesis I contribute to all three areas. In the area of structured estimation, I focus on models with low intrinsic dimensionality. I analyze the bias in Factor Analysis, the state-of-the-art factor model and propose Directional Variance Adjustment (DVA) Factor Analysis, which reduces bias and yields improved estimates of the covariance matrix.

Analytical shrinkage of Ledoit and Wolf (LW-Shrinkage) is the most popular regularized estimator. I contribute in three aspects: first, I provide a theoretical analysis of the behavior of LW-Shrinkage in the presence of pronounced eigendirections, a case of great practical relevance. I show that LW-Shrinkage does not perform well in this setting and propose aoc-Shrinkage which yields significant improvements. Second, I discuss the effect of autocorrelation on LW-Shrinkage and review the Sancetta-Estimator, an extension of LW-Shrinkage to autocorrelated data. I show that the Sancetta-Estimator is biased and propose a theoretically and empirically superior estimator with reduced bias. Third, I propose an extension of shrinkage to multiple shrinkage targets. Multi-Target Shrinkage is not restricted to covariance estimation and allows for many interesting applications which go beyond regularization, including transfer learning. I provide a detailed theoretical and empirical analysis.

Spectrum correction approaches the problem of covariance estimation by improving the estimates of the eigenvalues of the sample covariance matrix. I discuss the state-of-the-art approach, Nonlinear Shrinkage, and propose a cross-validation based covariance (CVC) estimator which yields competitive performance at increased numerical stability and greatly reduced complexity and computational cost. On all data sets considered, CVC is on par or superior in comparison to the regularized and structured estimators.

In the last chapter, I conclude with a discussion of the advantages and disadvantages of all covariance estimators presented in this thesis and give situation-specific recommendations. In addition, the appendix contains a systematic analysis of Linear Discriminant Analysis as a model application, which sheds light on the interdependency between the generative model of the data and various covariance estimators.

## Estimation of Theory-Implied Correlation Matrices [pdf](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3484152_code434076.pdf?abstractid=3484152&mirid=1)
Marcos Lopez de Prado

This paper introduces a machine learning (ML) algorithm to estimate forward-looking correlation matrices implied by economic theory. Given a particular theoretical representation of the hierarchical structure that governs a universe of securities, the method fits the correlation matrix that complies with that theoretical representation of the future. This particular use case demonstrates how, contrary to popular perception, ML solutions are not black-boxes, and can be applied effectively to develop and test economic theories.

## The Myth of Diversification Reconsidered [pdf](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3781844)
Kinlaw Kritzman Page and Turkington

That investors should diversify their portfolios is a core principle of modern finance. Yet there are some periods where diversification is undesirable. When the portfolio’s main growth engine performs well, investors prefer the opposite of diversification. An ideal complement to the growth engine would provide diversification when it performs poorly and unification when it performs well. Numerous studies have presented evidence of asymmetric correlations between assets. Unfortunately, this asymmetry is often of the undesirable variety: it is characterized by downside unification and upside diversification. In other words, diversification often disappears when it is most needed. In this article we highlight a fundamental flaw in the way that some prior studies have measured correlation asymmetry. Because they estimate downside correlations from subsamples where both assets perform poorly, they ignore instances of “successful” diversification; that is, periods where one asset’s gains offset the other’s losses. We propose instead that investors measure what matters: the degree to which a given asset diversifies the main growth engine when it underperforms. This approach yields starkly different conclusions, particularly for asset pairs with low full sample correlation. In this paper we review correlation mathematics, highlight the flaw in prior studies, motivate the correct approach, and present an empirical analysis of correlation asymmetry across major asset classes.

## A constrained hierarchical risk parity algorithm with cluster-based capital allocation [via](https://ideas.repec.org/p/sza/wpaper/wpapers328.html)
Johann Pfitzinger and Nico Ktazke

Hierarchical Risk Parity (HRP) is a risk-based portfolio optimisation algorithm, which has been shown to
generate diversified portfolios with robust out-of-sample properties without the need for a positive-definite
return covariance matrix (Lopez de Prado 2016). The algorithm applies machine learning techniques to identify
the underlying hierarchical correlation structure of the portfolio, allowing clusters of similar assets to compete for
capital. The resulting allocation is both well-diversified over risk sources and intuitively appealing. This paper
proposes a method of fully exploiting the information created by the clustering process, achieving enhanced
out-of-sample risk and return characteristics. In addition, a practical approach to calculating HRP weights
under box and group constraints is introduced. A comprehensive set of portfolio simulations over 6 equity
universes demonstrates the appeal of the algorithm for portfolios consisting of 20 − 200 assets. HRP delivers
highly diversified allocations with low volatility, low portfolio turnover and competitive performance metrics

## Schur Complement and Symmetric Positive Semidefinite Matrices [pdf](https://www.cis.upenn.edu/~jean/schur-comp.pdf)
Jean Gallier

In this note, we provide some details and proofs of some results from Appendix A.5 (especially
Section A.5.5) of Convex Optimization by Boyd and Vandenberghe. 


## Fast and accurate techniques for computing schur complements and performing numerical coarse graining [slides](https://amath.colorado.edu/faculty/martinss/Talks/2009_banff.pdf)
Gunnar Martinsson

## A Closer look at the Minimum-Variance Portfolio Optimization Model [pdf](https://downloads.hindawi.com/journals/mpe/2019/1452762.pdf)
Zhifeng Dai

Recently, by imposing the regularization term to objective function or additional norm constraint to portfolio weights, a number
of alternative portfolio strategies have been proposed to improve the empirical performance of the minimum-variance portfolio.
In this paper, we firstly examine the relation between the weight norm-constrained method and the objective function regularization method in minimum-variance problems by analyzing the Karush–Kuhn–Tucker conditions of their Lagrangian
functions. We give the range of parameters for the two models and the corresponding relationship of parameters. Given the range
and manner of parameter selection, it will help researchers and practitioners better understand and apply the relevant portfolio
models. We apply these models to construct optimal portfolios and test the proposed propositions by employing real market data

## Six Generalized Schur Complements [via](https://www.sciencedirect.com/science/article/pii/002437958890033X)
Butler and Morlay

We give a unified treatment of equivalence betwene some old and new generalizations of the Shcur complement of matrices

### G-Learner and GIRL: Goal Based Wealth Management with Reinfocement Learning [pdf](https://arxiv.org/abs/2002.10990)
Matthew Dixon and Igor Halperin

We present a reinforcement learning approach to goal based wealth management problems such as optimization of retirement plans or target dated funds. In such problems, an investor seeks to achieve a financial goal by making periodic investments in the portfolio while being employed, and periodically draws from the account when in retirement, in addition to the ability to re-balance the portfolio by selling and buying different assets (e.g. stocks). Instead of relying on a utility of consumption, we present G-Learner: a reinforcement learning algorithm that operates with explicitly defined one-step rewards, does not assume a data generation process, and is suitable for noisy data. Our approach is based on G-learning - a probabilistic extension of the Q-learning method of reinforcement learning.
In this paper, we demonstrate how G-learning, when applied to a quadratic reward and Gaussian reference policy, gives an entropy-regulated Linear Quadratic Regulator (LQR). This critical insight provides a novel and computationally tractable tool for wealth management tasks which scales to high dimensional portfolios. In addition to the solution of the direct problem of G-learning, we also present a new algorithm, GIRL, that extends our goal-based G-learning approach to the setting of Inverse Reinforcement Learning (IRL) where rewards collected by the agent are not observed, and should instead be inferred. We demonstrate that GIRL can successfully learn the reward parameters of a G-Learner agent and thus imitate its behavior. Finally, we discuss potential applications of the G-Learner and GIRL algorithms for wealth management and robo-advising


### Super Learner in Prediction [via](https://biostats.bepress.com/ucbbiostat/paper266/)
Eric Polley and Mark J. van der Laan

Super learning is a general loss based learning method that has been proposed and analyzed theoretically in van der Laan et al. (2007). In this article we consider super learning for prediction. The super learner is a prediction method designed to find the optimal combination of a collection of prediction algorithms. The super learner algorithm finds the combination of algorithms minimizing the cross-validated risk. The super learner framework is built on the theory of cross-validation and allows for a general class of prediction algorithms to be considered for the ensemble. Due to the previously established oracle results for the cross-validation selector, the super learner has been proven to represent an asymptotically optimal system for learning. In this article we demonstrate the practical implementation and finite sample performance of super learning in prediction.


### Ensemble Selection from Libraries of Models [pdf](https://www.cs.cornell.edu/~alexn/papers/shotgun.icml04.revised.rev2.pdf)
Caruna, Niculescu-Mizil, Crew and Ksikes

We present a method for constructing ensembles from libraries of thousands of models.
Model libraries are generated using different
learning algorithms and parameter settings.
Forward stepwise selection is used to add to
the ensemble the models that maximize its
performance. Ensemble selection allows ensembles to be optimized to performance metric such as accuracy, cross entropy, mean
precision, or ROC Area. Experiments with
seven test problems and ten metrics demonstrate the benefit of ensemble selection.

## Copula Based Portfolio Optimization [pdf](http://www.diva-portal.org/smash/get/diva2:1588992/FULLTEXT01.pdf)
Maziar Sahamkhadam

This thesis studies and develops copula-based portfolio optimization. The overall
purpose is to clarify the effects of copula modeling for portfolio allocation and
suggest novel approaches for copula-based optimization. The thesis is a compilation
of five papers. The first and second papers study and introduce copula-based
methods; the third, fourth, and fifth papers extend their applications to the BlackLitterman (BL) approach, expectile Value-at-Risk (EVaR), and multicriteria
optimization, respectively.


## Combining Portfolio Models [pdf](http://aeconf.com/Articles/Nov2014/aef150208.pdf)
Peter Schanbacher

The best asset allocation model is searched for. In this paper, we argue that
it is unlikely to find an individual model which continuously outperforms its
competitors. Rather one should consider a combined model out of a given set
of asset allocation models. In a large empirical study using various standard
asset allocation models, we find that (i) the best model depends strongly on
the chosen data set, (ii) it is difficult to ex-ante select the best model, and
(iii) the combination of models performs exceptionally well. Frequently, the
combination even outperforms the ex-post best asset allocation model. The
promising results are obtained by a simple combination method based on a
bootstrap procedure. More advanced combination approaches are likely to
achieve even better results.

## A Nested Factor Model for non-linear dependencies in stock returns [pdf](https://arxiv.org/pdf/1309.3102.pdf)
REMY CHICHEPORTICHE AND JEAN-PHILIPPE BOUCHAUD

The aim of our work is to propose a natural framework to account for all the empirically
known properties of the multivariate distribution of stock returns. We define and study a “nested factor
model”, where the linear factors part is standard, but where the log-volatility of the linear factors and
of the residuals are themselves endowed with a factor structure and residuals. We propose a calibration
procedure to estimate these log-vol factors and the residuals. We find that whereas the number of
relevant linear factors is relatively large (10 or more), only two or three log-vol factors emerge in our
analysis of the data. In fact, a minimal model where only one log-vol factor is considered is already very
satisfactory, as it accurately reproduces the properties of bivariate copulas, in particular the dependence
of the medial-point on the linear correlation coefficient, as reported in Chicheportiche and Bouchaud
(2012). We have tested the ability of the model to predict Out-of-Sample the risk of non-linear portfolios,
and found that it performs significantly better than other schemes.

## A Forecast Comparison of Volatility Models [pdf](http://faculty.washington.edu/ezivot/econ589/DoesAnythingBeatGarch11.pdf)
Hansen and Lunde

By using intra-day returns to calculate a measure for the time-varying volatility, Andersen and Bollerslev (1998a) established that volatility models do provide good forecasts of the conditional variance. In this paper, we take the same approach and use intra-day estimated measures of volatility to compare volatility models. Our objective is to evaluate whether the evolution of volatility models has led to better forecasts of volatility when compared to the first “species” of volatility models. We make an out-of-sample comparison of 330 different volatility models using daily exchange rate data (DM/$) and IBM stock prices. Our analysis does not point to a single winner amongst the different volatility models, as it is different models that are best at forecasting the volatility of the two types of assets. Interestingly, the best models do not provide a significantly better forecast than the GARCH(1,1) model.


## Bayesian Inference for Correlations in the Presence of Measurement Error and Estimation Uncertainty [pdf](http://www.alexander-ly.com/wp-content/uploads/2014/09/MatzkeEtAl2016NoisyCorrelations.pdf) also [pdf](https://arxiv.org/pdf/1510.01188.pdf)
Dora Matzke1, Alexander Ly1, Ravi Selker , Wouter D. Weeda, Benjamin Scheibehenne, Michael D. Lee, and Eric-Jan Wagenmakers

Whenever parameter estimates are uncertain or observations are contaminated by measurement error, the Pearson correlation coefficient can severely underestimate the true
strength of an association. Various approaches exist for inferring the correlation in the
presence of estimation uncertainty and measurement error, but none are routinely applied
in psychological research. Here we focus on a Bayesian hierarchical model proposed by
Behseta, Berdyyeva, Olson, and Kass (2009) that allows researchers to infer the underlying
correlation between error-contaminated observations. We show that this approach may be
also applied to obtain the underlying correlation between uncertain parameter estimates
as well as the correlation between uncertain parameter estimates and noisy observations.
We illustrate the Bayesian modeling of correlations with two empirical data sets; in each
data set, we first infer the posterior distribution of the underlying correlation and then
compute Bayes factors to quantify the evidence that the data provide for the presence of
an association

## Optimizing the Omega Ratio using Linear Programming [pdf](https://cs.uwaterloo.ca/~yuying/Courses/CS870_2012/Omega_paper_Short_Cm.pdf)
Kapsos et al

The Omega Ratio is a recent performance measure. It captures both, the downside and upside potential of
the constructed portfolio, while remaining consistent with utility maximization. In this paper, a new approach to
compute the maximum Omega Ratio as a linear program is derived. While the Omega ratio is considered to be
a non-convex function, we show an exact formulation in terms of a convex optimization problem, and transform
it as a linear program. The convex reformulation for the Omega Ratio maximization is a direct analogue to
mean-variance framework and the Sharpe Ratio maximization.
