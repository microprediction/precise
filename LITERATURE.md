In no particular order. The scope is robust diversified portfolios and things that help. To add to this list or correct an entry, ideally:

   1. Fork the repo (top right)
   2. Edit this file. 
   3. Submit a pull request (also possible with a click or two).
  
Or file an [issue](https://github.com/microprediction/precise/issues).  


## A Mean/Variance Analysis of Tracking Error [pdf](https://www.anderson.ucla.edu/documents/areas/fac/finance/1992-2.pdf)
Richard Roll 

Minimizing the volatility of tracking error will not produce a more efficient managed portfolio.

## Passive Investment Styles [pdf](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5024011)
Tom Ernst, Monika Gehde-Trapp, Holger Kraft

Passive investment funds hold cash, for example to honor redemption claims. We show that in the presence of cash there is no uniquely optimal passive strategy. Instead a trade-off arises: Minimizing tracking error generates a return gap, whereas closing this gap increases tracking error. This gives rise to different passive investment styles. We theoretically and empirically document that three different styles exist, which cater to three different investor types. Furthermore, the existence of cash inevitably leads to deviations from the benchmark (positive and negative) if a fund minimizes tracking error. As a consequence, the passive industry as a whole generates a heterogeneous price impact in the cross section of stock returns resulting from these deviations.



## Trans-Glasso: A Transfer Learning Approach to Precision Matrix Estimation [arxiv](https://arxiv.org/pdf/2411.15624)
Boxin Zhao1, Cong Ma2 , and Mladen Kolar

Precision matrix estimation is essential in various fields, yet it is challenging when
samples for the target study are limited. Transfer learning can enhance estimation accuracy by leveraging data from related source studies. We propose Trans-Glasso, a two-step
transfer learning method for precision matrix estimation. First, we obtain initial estimators using a multi-task learning objective that captures shared and unique features
across studies. Then, we refine these estimators through differential network estimation
to adjust for structural differences between the target and source precision matrices.
Under the assumption that most entries of the target precision matrix are shared with
source matrices, we derive non-asymptotic error bounds and show that Trans-Glasso
achieves minimax optimality under certain conditions. Extensive simulations demonstrate Trans-Glasso ’s superior performance compared to baseline methods, particularly
in small-sample settings. We further validate Trans-Glasso in applications to gene networks across brain tissues and protein networks for various cancer subtypes, showcasing
its effectiveness in biological contexts. Additionally, we derive the minimax optimal rate
for differential network estimation, representing the first such guarantee in this area.

## Graph-Based Methods for Forecasting Realized Covariances  [JoFE](https://academic.oup.com/jfec/advance-article/doi/10.1093/jjfinec/nbae026/7889003?login=false)
Chao Zhang, Xingyue Pu, Mihai Cucuringu, Xiaowen Dong

We forecast the realized covariance matrix of asset returns in the U.S. equity market by exploiting the predictive information of graphs in volatility and correlation. Specifically, we augment the Heterogeneous Autoregressive model via neighborhood aggregation on these graphs. Our proposed method allows for the modeling of interdependence in volatility (also known as spillover effect) and correlation, while maintaining parsimony and interpretability. We explore various graph construction methods, including sector membership and graphical LASSO (for modeling volatility), and line graph (for modeling correlation). The results generally suggest that the augmented model incorporating graph information yields both statistically and economically significant improvements for out-of-sample performance over the traditional models. Such improvements remain significant over horizons up to 1 month ahead, but decay in time. The robustness tests demonstrate that the forecast improvements are obtained consistently over the different out-of-sample sub-periods and are insensitive to measurement errors of volatilities.


## Squeezing Financial Noise: A Novel Approach to Covariance Matrix Estimation [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4986939)
Sander Gerber et al

We introduce a technique which can be used to manipulate the noise present in financial data in order to better estimate a covariance matrix. The technique, which we refer to as squeezing, parameterizes statistical distributional alignment so that we can vectorize co-movement noise. Squeezing underpins a novel approach to portfolio optimization in which the covariance matrix may be determined on an objective-specific basis. Our model-free approach more fully explores the eigenspace of the estimated matrix and is applicable across the dimensionality range of portfolio size and concentration. Squeezing is shown to outperform popular techniques used to treat noise in financial covariance matrices

## Universal Portfolios [pdf](https://web.mit.edu/6.454/www/www_fall_2001/shaas/universal_portfolios.pdf)
Tom Cover

We exhibit an algorithm for portfolio selection that asymptotically outperforms the best stock in the market. 


## Shrinking the eigenvalues of M-estimators of covariance matrix [pdf](https://arxiv.org/pdf/2006.10005)
Daniel P. Palomar, Frederic Pascal

A highly popular regularized (shrinkage) covariance
matrix estimator is the shrinkage sample covariance matrix
(SCM) which shares the same set of eigenvectors as the SCM but
shrinks its eigenvalues toward the grand mean of the eigenvalues
of the SCM. In this paper, a more general approach is considered
in which the SCM is replaced by an M-estimator of scatter
matrix and a fully automatic data adaptive method to compute
the optimal shrinkage parameter with minimum mean squared
error is proposed. Our approach permits the use of any weight
function such as Gaussian, Huber’s, Tyler’s, or t weight functions,
all of which are commonly used in M-estimation framework. Our
simulation examples illustrate that shrinkage M-estimators based
on the proposed optimal tuning combined with robust weight
function do not loose in performance to shrinkage SCM estimator
when the data is Gaussian, but provide significantly improved
performance when the data is sampled from an unspecified
heavy-tailed elliptically symmetric distribution. Also, real-world
and synthetic stock market data validate the performance of the
proposed method in practical applications


## The Factorization of Sparse Symmetric Indefinite Matrices [pdf](https://www.numerical.rl.ac.uk/media/people/nick-gould/DuffGoulReidScot91_imajna.pdf)
Duff et al

The Harwell multifrontal code MA27 is able to solve symmetric indefinite systems
of linear equations such as those that arise from least-squares and constrained
optimization algorithms, but may sometimes lead to many more arithmetic
operations being needed to factorize the matrix than is required by other
strategies. In this paper, we report on the results of our investigation of this
problem. We have concentrated on seeking new strategies that preserve the
multifrontal principle but follow the sparsity structure more closely in the case
when some of the diagonal entries are zero.


## Constrained Max Drawdown [pdf](https://arxiv.org/pdf/2401.02601)
Albert Dorador

We propose an alternative linearization to the classical Markowitz quadratic portfolio optimization model, based on maximum drawdown. This model, which minimizes maximum portfolio drawdown, is particularly appealing during times of financial distress, like during the COVID-19 pandemic. In addition, we will present a Mixed-Integer Linear Programming variation of our new model that, based on our out-of-sample results and sensitivity analysis, delivers a more profitable and robust solution with a 200 times faster solving time compared to the standard Markowitz quadratic formulation.

## Geodesically Parametrized Covariance Estimation [pdf](https://arxiv.org/pdf/2001.01805)
ANTONI MUSOLAS, STEVEN T. SMITH, AND YOUSSEF MARZOUK

Statistical modeling of spatiotemporal phenomena often requires selecting a covariance matrix from
a covariance class. Yet standard parametric covariance families can be insufficiently flexible for practical applications, while non-parametric approaches may not easily allow certain kinds of prior knowledge to be incorporated. We propose instead to build covariance families out of geodesic curves. These covariances offer more flexibility for problem-specific tailoring than classical parametric families, and are preferable to simple convex combinations. Once the covariance family has been chosen, one typically needs to select a representative member by solving an optimization problem, e.g., by maximizing the likelihood of a data set. We consider instead a differential geometric interpretation of this problem: minimizing the geodesic distance to a sample covariance matrix (“natural projection”). Our approach is consistent with the notion of distance employed to build the covariance family and does not require assuming a particular probability distribution for the data. We show that natural projection and maximum likelihood estimation within the covariance family are locally equivalent up to second order. We also demonstrate
that natural projection may yield more accurate estimates with noise-corrupted data

## Portfolio Optimization. Theory and Application (Book) [html](https://bookdown.org/palomar/portfoliooptimizationbook/)
Daniel P. Palomar

This book explores practical financial data modeling and portfolio optimization, covering a wide range of variations and extensions. It systematically starts with mathematical formulations and proceeds to develop practical numerical algorithms, supplemented with code examples to enhance understanding.

## Efficient and Scalable Parametric High-Order Portfolios Design via the Skew-t Distribution [pdf](https://palomar.home.ece.ust.hk/papers/2023/WangZhouYingPalomar-TSP2023.pdf)
Xiwen Wang , Rui Zhou, Jiaxi Ying , and Daniel P. Palomar

Since Markowitz’s mean-variance framework, optimizing a portfolio that strikes a trade-off between maximizing profit and minimizing risk has been ubiquitous in the financial industry. Initially, profit and risk were measured by the first two moments of the portfolio’s return, a.k.a. the mean
and variance, which are sufficient to characterize a Gaussian
distribution. However, it is broadly believed that the first two
moments are not enough to capture the characteristics of the
returns’ behavior, which have been recognized to be asymmetric
and heavy-tailed. Although portfolio designs involving the third
and fourth moments, i.e., skewness and kurtosis, have been
demonstrated to outperform the conventional mean-variance
framework, they present non-trivial challenges. Specifically, in
the classical framework, the memory and computational cost
of computing the skewness and kurtosis grow sharply with the
number of assets. To alleviate the difficulty in high-dimensional
problems, we consider an alternative expression for high-order
moments based on parametric representations via a generalized
hyperbolic skew-t distribution. Then, we reformulate the highorder portfolio optimization problem as a fixed-point problem and propose a robust fixed-point acceleration algorithm that
solves the problem in an efficient and scalable manner. Empirical
experiments also attest to the efficiency of our proposed highorder portfolio optimization framework, which presents low complexity and significantly outperforms the state-of-the-art
methods by 2 ∼ 4 orders of magnitude

## Optimal Portfolio Size under Parameter Uncertainty [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4886000)
Nathan Lassance, Rodolphe Vanderveken,Frédéric D. Vrins

Estimation risk in portfolio selection can be mitigated with sparse approaches such as lasso that penalizes for the norm of the portfolio weights and excludes assets from the investment universe. The latter are revealed a posteriori, by identifying which assets receive an optimal weight of zero. We show instead that in the presence of parameter uncertainty, it is desirable to remove assets before computing the portfolio weights. In particular, we show that the optimal portfolio size strikes a tradeoff between accessing additional investment opportunities and limiting estimation risk. Our approach disentangles the determination of the optimal portfolio size from the asset selection rule, making it more easily implementable and robust to estimation risk than alternative sparse methods. Empirically, our restricted portfolios substantially outperform their counterparts applied to all available assets. Our methodology renders portfolio theory valuable even when the full dataset dimension is comparable to the sample size.

## Optimal Portfolio Diversification via Independent Component Analysis [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3285156)
Nathan Lassance, Victor DeMiguel, Frédéric D. Vrins

A natural approach to enhance portfolio diversification is to rely on factor-risk parity, which yields the portfolio whose risk is equally spread among a set of uncorrelated factors. The standard choice is to take the variance as risk measure, and the principal components (PCs) of asset returns as factors. Although PCs are unique and useful for dimension reduction, they are an arbitrary choice: any rotation of the PCs results in uncorrelated factors. This is problematic because we demonstrate that any portfolio is a factor-variance-parity portfolio for some rotation of the PCs. More importantly, choosing the PCs does not account for the higher moments of asset returns. To overcome these issues, we propose to use the independent components (ICs) as factors, which are the rotation of the PCs that are maximally independent, and care about higher moments of asset returns. We demonstrate that using the IC-variance-parity portfolio helps to reduce the return kurtosis. We also show how to exploit the near independence of the ICs to parsimoniously estimate the factor-risk-parity portfolio based on Value-at-Risk. Finally, we empirically demonstrate that portfolios based on ICs outperform those based on PCs, and several state-of-the-art benchmarks.

## Robust Portfolio Selection Based on Copula Change Analysis [via](https://www.researchgate.net/publication/331394689_Robust_Portfolio_Selection_Based_on_Copula_Change_Analysis)

Yingwei Han, Ping Li, Jie Li, Sanmang Wu

In this article, we construct a robust portfolio selection model based on dynamic copulas. We first use a type of dynamic copula, which contains copulas with time-varying parameters or sequence of copulas, to characterize the dynamic dependence between financial assets. Then, we use it for portfolio selection based on worst-case Conditional Value-at-Risk (WCVaR). In the empirical part we choose four representative assets from Chinese market to construct a macro asset allocation of portfolio and make the performance analysis. Results show that our method performs the best in out-of-sample tests when considering the dynamic dependence between assets and the uncertainty in the estimated model.

## A new distributionally robust reward-risk model for portfolio optimization [pdf](https://www.degruyter.com/document/doi/10.1515/math-2024-0010/pdf?licenseType=open-access)
Yijia Zhou and Lijun Xu 

A new distributionally robust ratio optimization model is proposed under the known first and second moments of the uncertain distributions. In this article, both standard deviation (SD) and conditional value-at-risk (CVaR) are used to measure the risk, avoiding both fat-tail and volatility. The new model can be reduced to a simple distributionally robust model under assumptions on the measurements of reward, CVaR and SD. Furthermore, it can be rewritten as a tractable semi-definite programming problem by the duality theorem under partially known information of the uncertain parameters. Finally, the model is tested on portfolio problems and verified from numerical results that it can give a reasonable decision under only the first and second moments.


## Robust and Sparse Portfolio: Optimization Models and Algorithms [pdf](https://www.mdpi.com/2227-7390/11/24/4925)
Hongxin Zhao, Yilun Jiang, and Yizhou Yang

The robust and sparse portfolio selection problem is one of the most-popular and -frequently studied problems in the optimization and financial literature. By considering the uncertainty of the parameters, the goal is to construct a sparse portfolio with low volatility and decent returns, subject to other investment constraints. In this paper, we propose a new portfolio selection model, which considers the perturbation in the asset return matrix and the parameter uncertainty in the expected asset return. We define three types of stationary points of the penalty problem: the Karush–Kuhn–Tucker point, the strong Karush–Kuhn–Tucker point, and the partial minimizer. We analyze the relationship between these stationary points and the local/global minimizer of the penalty model under mild conditions. We design a penalty alternating-direction method to obtain the solutions. Compared with several existing portfolio models on seven real-world datasets, extensive numerical experiments demonstrate the robustness and effectiveness of our model in generating lower volatility.

## Robust Multi-period Portfolio Selection Based on Downside Risk with Asymmetrically Distributed Uncertainty Set [pdf](https://www.researchgate.net/publication/330326468_Robust_Multi-period_Portfolio_Selection_Based_on_Downside_Risk_with_Asymmetrically_Distributed_Uncertainty_Set)

Aifan Ling, Jie Sun, Meihua Wang

Motivated by the asymmetrical attitudes of investors towards downside losses and upside gains, this paper proposes a robust multi-period portfolio selection model based on downside risk with asymmetrically distributed uncertainty set, in which the downside losses of a portfolio are controlled by the lower partial moment (LPM). A computationally tractable approximation approach based on second-order cone optimization is used for solving the proposed model. We show in theory that the optimal solution of the robust model can generate a given probability guarantee for individual and joint stochastic constraints. The effect of the asymmetrically distributed uncertainty set on performance of the optimal solution is analyzed by the usual comparative static method. Comprehensive numerical comparisons with real market data are reported and indicate that the proposed model can obtain the smaller standard deviation and turnover ratios which reduce the Sharpe ratios of optimal portfolio, compared with some well-known models in the literature.


## Risk Parity Portfolio Optimization under Heavy-Tailed Returns and Time-Varying Volatility [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4652551)
Marc S. Paolella, Pawel Polak, Patrick S. Walker

Risk parity portfolio optimization, using expected shortfall as the risk measure, is investigated when asset returns are fat-tailed and heteroscedastic. The conditional return distribution is modeled by an elliptical multivariate generalized hyperbolic distribution, allowing for fast parameter estimation, via an expectation-maximization algorithm and a semi-closed form of the risk contributions. The efficient computation of non-Gaussian risk parity weights sidesteps the need for numerical simulations or Cornish-Fisher-type approximations. Accounting for fat-tailed returns, the risk parity allocation is less sensitive to volatility shocks, thereby generating lower portfolio turnover, in particular during market turmoils such as the global financial crisis. Although risk parity portfolios are surprisingly robust to the misuse of the Gaussian distribution, a more realistic model for conditional returns and time-varying volatilies can improve risk-adjusted returns, reduces turnover during periods of market stress and enables the use of a holistic risk model for portfolio and risk management.

## The 1/N investment strategy is optimal under high model ambiguity [pdf](https://www-user.tu-chemnitz.de/~alopi/publications/uniformInvestRevision.pdf)
Georg Ch. Pfluga, Alois Pichlera, David Wozabalb

The 1/N investment strategy, i.e. the strategy to split one’s wealth uniformly between the
available investment possibilities, recently received plenty of attention in the literature. In
this paper, we demonstrate that the uniform investment strategy is rational in situations where
an agent is faced with a sufficiently high degree of model uncertainty in the form of ambiguous
loss distributions. More specifically, we use a classical risk minimization framework to show
that, for a broad class of risk measures, as the uncertainty concerning the probabilistic model
increases, the optimal decisions tend to the uniform investment strategy. To illustrate the theoretical results of the paper, we investigate the Markowitz portfolio
selection model as well as Conditional Value-at-Risk minimization with ambiguous loss distributions. Subsequently, we set up a numerical study using real market data to demonstrate the
convergence of optimal portfolio decisions to the uniform investment strategy

## On robust mean-variance portfolios [pdf](https://repository.bilkent.edu.tr/server/api/core/bitstreams/79bb8dd8-46d0-48ba-91eb-6ce2b400f77c/content)
Mustafa Ç. Pınar

We derive closed-form portfolio rules for robust mean–variance portfolio
optimization where the return vector is uncertain or the mean return
vector is subject to estimation errors, both uncertainties being confined
to an ellipsoidal uncertainty set. We consider different mean–variance
formulations allowing short sales, and derive closed-form optimal portfolio
rules in static and dynamic settings.

## Mean semi-deviation from a target and robust portfolio choice under distribution and mean return ambiguity [pdf](https://core.ac.uk/download/pdf/52923773.pdf)
Mustafa Ç. Pınar, A. Burak Paç

We consider the problem of optimal portfolio choice using the lower partial moments
risk measure for a market consisting of n risky assets and a riskless asset. For when the
mean return vector and variance/covariance matrix of the risky assets are specified without
specifying a return distribution, we derive distributionally robust portfolio rules. We then
address potential uncertainty (ambiguity) in the mean return vector as well, in addition to
distribution ambiguity, and derive a closed-form portfolio rule for when the uncertainty in
the return vector is modelled via an ellipsoidal uncertainty set. Our result also indicates a
choice criterion for the radius of ambiguity of the ellipsoid. Using the adjustable robustness
paradigm we extend the single-period results to multiple periods, and derive closed-form
dynamic portfolio policies which mimic closely the single-period policy

## Essays on Robust Portfolio Management [pdf](https://www.e-helvetica.nb.admin.ch/api/download/urn%3Anbn%3Ach%3Abel-1412461%3ADis4910.pdf/Dis4910.pdf)
Lukas Plachel

Chapter 1 addresses the problems of traditional mean-variance optimization originating from model- and estimation errors. In order to simultaneously tackle both
error sources, a joint method for covariance regularization and robust optimization
is proposed which exploits the inherent complementarity between the two concepts.
Chapter 2 introduces a covariance estimation approach which is based solely on
characteristic company information. In contrast to traditional, time series based estimation procedures which typically lead to extreme and unreliable estimates, the proposed method produces stable covariance matrices which can be used if no time series
data is available, or complementary to traditional methods. We derive characteristicsbased covariance matrices for a US stock universe and use them as shrinkage targets in
a minimum variance optimization example. 
Chapter 3 bridges the gap between MPT and one of the most vivid fields of contemporary research: Artificial Intelligence. A model is introduced which uses a Neural
Network to learn the relation between portfolio weights and arbitrary measures of
portfolio success. Based on the resulting approximation function, a Genetic Algorithm is employed to derive a near-optimal allocation. Two portfolio selection examples for the commodity and the equity market illustrate the potential to successfully
implement a wide scope of traditional and exotic investment strategies.

## Robust Growth-Optimal Portfolios [pdf](https://core.ac.uk/download/pdf/76990543.pdf)
Napat Rujeerapaiboon

A portfolio which has a maximum expected growth rate is often referred to in the literature as a logoptimal portfolio or a growth-optimal portfolio. The origin of the log-optimal portfolio is arguably
due to Kelly when he observed that logarithmic wealth is additive in sequential investments and
invented a betting strategy for gambling that relies on results from information theory. As a result of
the law of large numbers, if investment returns are serially independent and identically distributed,
the growth rate of any constant rebalanced portfolio (the log-optimal portfolio included) converges
to its expectation. Moreover, under such conditions, one of the strongest advantages of the logoptimal portfolio is that, when implemented repeatedly, the log-optimal portfolio outperforms any
other causal portfolio in the long run with probability 1. In other words, if all of these conditions
are met, there is no sequence of portfolios that has a higher growth rate than that of the log-optimal
portfolio. Stock markets however are different from casinos in the sense that investment returns are
not serially independent and identically distributed. Also, since trading incurs transaction costs,
investors are discouraged from making frequent trades. Plus, the probability distribution of stock
returns is never precisely known, which impedes the calculation of the log-optimal portfolio. In
this project, we generalize the results for the log-optimal portfolio. In particular, we establish similar guarantees for finite investment horizons where the distribution of stock returns is ambiguous.
By focusing on constant rebalanced portfolios, we exploit temporal symmetries to formulate the
emerging distributionally robust optimization problems as tractable conic programs whose sizes are
independent of the investment horizon.

## Portfolio Optimization and Parameter Uncertainty [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4709317) [code](https://os.fortitudo.tech)
Laura Kristensen and Anton Vorobets

Portfolio optimization has a mixed reputation among investment managers, with some being so skeptical that they believe it is almost useless due to the inherent parameter uncertainty. It is undeniable that portfolio optimization problems are sensitive to parameter estimates, especially the expected returns that are arguably also the hardest parameters to estimate. However, most practitioners still attempt to build mean-risk optimal portfolios, albeit in implicit ways. Resampled optimization is a popular mathematical heuristic to tackle the parameter uncertainty issue. It computes optimal portfolios using sampled parameter estimates and calculates a simple average of the portfolio exposures across samples. The unsatisfactory aspect of the resampled approach is that there is no mathematical justification for using the average of portfolio exposures, it just works well in practice. This article provides perspectives for understanding the resampling approach by analyzing the portfolio exposure estimation process from a bias-variance trade-off. We show that the traditional resampled optimization corresponds to a naive version of stacked generalization. Finally, we introduce a stacked generalization approach that can be used to handle both parameter uncertainty and combine optimization methods in full generality. We coin the new method Exposure Stacking.


## Distributionally Robust Reward-risk Ratio Programming with Wasserstein Metric [pdf](https://optimization-online.org/wp-content/uploads/2017/01/5805.pdf)
Yong Zhao, Yongchao Liu, Jin Zhang, Xinmin Yang

Reward-risk ratio (RR) is a very important stock market definition. In order to capture the
situation that the investor does not have complete information on the distribution of the underlying
uncertainty, people extend RR model to distributionally robust reward-risk ratio (DRR) model. In this
paper, we study the DRR problem where the ambiguity on the distributions is defined through Wassertein
metric. Under some moderate conditions, we show that for a fixed ratio, the DRR problem has the
tractable reformulation, which means that we may solve the problem by bisection method. Specifically,
we analyze the DRR problems for Sortino-Satchel ratio, Stable Tail Adjusted Return ratio and Omega
ratio.

## Robust minimum variance portfolio optimization modelling under scenario uncertainty [pdf](https://isiarticles.com/bundles/Article/pre/pdf/111157.pdf)
Panos Xidonasa, Christis Hassapis, John Soulisc, Aristeidis Samitasd

Our purpose in this article is to develop a robust optimization model which minimizes portfolio variance for a
finite set of covariance matrices scenarios. The proposed approach aims at the proper selection of portfolios, in a
way that for every covariance matrix estimate included in the analysis, the calculated portfolio variance remains
as close to the corresponding individual minimum value, as possible. To accomplish this, we formulate a mixedinteger non-linear program with quadratic constraints. With respect to practical underlying concerns,
investment policy constraints regarding the portfolio structure are also taken into consideration. The validity
of the proposed approach is verified through extensive out-of-sample empirical testing in the EuroStoxx 50, the
S & P 100, the S & P 500, as well as a well-diversified investment universe of ETFs. We report consistent
generation of stable out-of-sample returns, which are in most cases superior to those of the worst-case scenario.
Moreover, we provide strong evidence that the proposed robust model assists in selective asset picking and
systematic avoidance of excessive losses.


## Robust portfolio optimization: a categorized bibliographic review [pdf](https://www.terry.uga.edu/wp-content/uploads/Robust.pdf)
Panos Xidonas, Ralph Steuer, Christis Hassapis

Robust portfolio optimization refers to finding an asset allocation strategy whose behavior
under the worst possible realizations of the uncertain inputs, e.g., returns and covariances, is
optimized. The robust approach is in contrast to the classical approach, where one estimates
the inputs to a portfolio allocation problem and then treats them as certain and accurate. In
this paper we provide a categorized bibliography on the application of robust mathematical
programming to the portfolio selection problem. With no similar surveys available, one of
the aims of this review is to provide quick access for those interested, but maybe not yet in the
area, so they know what the area is about, what has been accomplished and where everything
can be found. Toward this end, a total of 148 references have been compiled and classified
in various ways. Additionally, the number of Scopus© citations by contribution and journal
is recorded. Finally, a brief discussion of the review’s major findings is provided and some
solid leads on future directions are given.

## Regime-dependent Robust Risk Measures with Application in Portfolio Selection [via](https://www.researchgate.net/publication/262691745_Regime-dependent_Robust_Risk_Measures_with_Application_in_Portfolio_Selection)
Jia Liu, Zhiping Chen

Current robust risk measures or portfolio selection models are usually derived under the worst-case analysis, which makes the investment decision too conservative and could not reflect the change of uncertainty sets with respect to different market environ- ments. We use the regime switching technique to describe the time-varying uncertainty set of the first and second order moments, and propose two kinds of robust risk measures: worst regime risk measure and mixed worst-case risk measure. These new risk measures have good properties and the robust portfolio selection models derived from them can be efficiently solved in polynomial time. Empirical results show the reasonability and efficiency of our new models.

## Robust Portfolio Rebalancing with Cardinality and Diversification Constraints [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3808694)
Zhihua Allen-Zhao, Fengmin Xu, Donglei Du, Meihua Wang

In this paper, we develop a robust conditional value at risk (CVaR) optimal portfolio rebalancing model under various financial constraints to construct sparse and diversified rebalancing portfolios. Our model includes transaction costs and double cardinality constraints in order to capture the trade-off between the limit of investment scale and the diversified industry coverage requirement. We first derive a closed-form solution for the robust CVaR portfolio rebalancing model with only transaction costs. It allows us to conduct industry risk analysis for sparse portfolio rebalancing in the absence of diversification constraints. Then, we attempt to remedy the hidden industry risk by establishing a new robust portfolio rebalancing model with both sparse and diversified constraints. This is followed by the development of a distributed-version of the Alternating Direction Method of Multipliers (ADMM) algorithm, where each subproblem admits a closed-form solution. Finally, we conduct empirical tests to compare our proposed strategy with the standard sparse rebalancing and no-rebalancing strategies. The computational results demonstrate that our rebalancing approach produces sparse and diversified portfolios with higher industry coverage. Additionally, to measure out-of-sample performance, two superiority indices are created based on the worst-case CVaR and annualized return, respectively. Our ADMM strategy also outperforms the sparse rebalancing and no-rebalancing strategies in terms of the two indices.

## Portfolio management with robustness in both prediction and decision: A mixture model based learning approach [pdf](https://isiarticles.com/bundles/Article/pre/pdf/49455.pdf)
Shushang Zhu, Minjie Fan, Duan Li

We develop in this paper a novel portfolio selection framework with a feature of double
robustness in both return distribution modeling and portfolio optimization. While predicting
the future return distributions always represents the most compelling challenge in investment,
any underlying distribution can be always well approximated by utilizing a mixture distribution, if we are able to ensure that the component list of a mixture distribution includes all
possible distributions corresponding to the scenario analysis of potential market modes.
Adopting a mixture distribution enables us to (1) reduce the problem of distribution prediction
to a parameter estimation problem in which the mixture weights of a mixture distribution are
estimated under a Bayesian learning scheme and the corresponding credible regions of the
mixture weights are obtained as well and (2) harmonize information from different channels,
such as historical data, market implied information and investors' subjective views. We further
formulate a robust mean-CVaR portfolio selection problem to deal with the inherent
uncertainty in predicting the future return distributions. By employing the duality theory, we
show that the robust portfolio selection problem via learning with a mixture model can be
reformulated as a linear program or a second-order cone program, which can be effectively
solved in polynomial time. We present the results of simulation analyses and primary empirical
tests to illustrate a significance of the proposed approach and demonstrate its pros and cons.

## Data-driven distributionally robust optimization using the wasserstein metric: Performance guarantees and tractable reformulations [pdf](https://arxiv.org/pdf/1505.05116)
PEYMAN MOHAJERIN ESFAHANI AND DANIEL KUHN

We consider stochastic programs where the distribution of the uncertain parameters is only observable through a finite training dataset. Using the Wasserstein metric, we construct a ball in the space of
(multivariate and non-discrete) probability distributions centered at the uniform distribution on the training samples, and we seek decisions that perform best in view of the worst-case distribution within this
Wasserstein ball. The state-of-the-art methods for solving the resulting distributionally robust optimization
problems rely on global optimization techniques, which quickly become computationally excruciating. In this
paper we demonstrate that, under mild assumptions, the distributionally robust optimization problems over
Wasserstein balls can in fact be reformulated as finite convex programs—in many interesting cases even as
tractable linear programs. Leveraging recent measure concentration results, we also show that their solutions
enjoy powerful finite-sample performance guarantees. Our theoretical results are exemplified in mean-risk
portfolio optimization as well as uncertainty quantification.

## Robust and Sparse Portfolio: Optimization Models and Algorithms [via](https://www.researchgate.net/publication/376420963_Robust_and_Sparse_Portfolio_Optimization_Models_and_Algorithms)
Hongxin Zhao, Yilun Jiang, Yizhou Yang

The robust and sparse portfolio selection problem is one of the most-popular and -frequently studied problems in the optimization and financial literature. By considering the uncertainty of the parameters, the goal is to construct a sparse portfolio with low volatility and decent returns, subject to other investment constraints. In this paper, we propose a new portfolio selection model, which considers the perturbation in the asset return matrix and the parameter uncertainty in the expected asset return. We define three types of stationary points of the penalty problem: the Karush–Kuhn–Tucker point, the strong Karush–Kuhn–Tucker point, and the partial minimizer. We analyze the relationship between these stationary points and the local/global minimizer of the penalty model under mild conditions. We design a penalty alternating-direction method to obtain the solutions. Compared with several existing portfolio models on seven real-world datasets, extensive numerical experiments demonstrate the robustness and effectiveness of our model in generating lower volatility.

## Some connections between higher moments portfolio optimization methods [pdf](https://arxiv.org/pdf/2201.00205)
Farshad Noravesh1 Kristiaan Kerstens 

In this paper, different approaches to portfolio optimization having
higher moments such as skewness and kurtosis are classified so that
the reader can observe different paradigms and approaches in this
field of research which is essential for practitioners in Hedge Funds
in particular. Several methods based on different paradigms such as
utility approach and multi-objective optimization are reviewed and
the advantage and disadvantageous of these ideas are explained. 

## Incorporating estimation errors into portfolio selection: Robust portfolio construction [via](https://www.researchgate.net/publication/228380747_Incorporating_estimation_errors_into_portfolio_selection_Robust_portfolio_construction)
Sebastián Ceria and Robert A. Stubbs

The authors explore the negative effect that estimation error has on mean-variance optimal portfolios. It is shown that asset weights in mean-variance optimal portfolios are very sensitive to slight changes in input parameters. This instability is magnified by the presence of constrains that asset managers typically impose on their portfolios. The authors propose to use robust mean variance, a new technique which is based on robust optimisation, a deterministic framework designed to explicitly consider parameter uncertainty in optimisation problems. Alternative uncertainty regions that create a less conservative robust problem are introduced. In fact, the authors' proposed approach does not assume that all estimation errors will negatively affect the portfolios, as is the case in traditional robust optimisation, but rather that there are as many errors with negative consequences as there are errors with positive consequences. The authors demonstrate through extensive computational experiments that portfolios generated with their proposed robust mean variance methodolgy typically outperform traditional mean variance portfolios in a variety of investment scenarios. Additionally, robust mean variance portfolios are usually less sensitive to input parameters.

## Robust Portfolio Optimization with Correlation Penalties [pdf](https://kth.diva-portal.org/smash/get/diva2:1816894/FULLTEXT01.pdf)
Pelle Nydahl

Robust portfolio optimization models attempt to address the standard optimization method’s
high sensitivity to noise in the parameter estimates, by taking an investor’s uncertainty
about the estimates into account when finding an optimal portfolio. In this thesis, we
study robust variations of an extension of the mean-variance problem, where an additional
term penalizing the portfolio’s correlation with an exogenous return sequence is included
in the objective. Using a normalized risk factor model of the asset returns, estimations are
done using EMA filtering as well as exponentially weighted linear regression. We show that
portfolio performance can significantly improve with respect to a range of metrics, such as
Sharpe ratio, expected shortfall and skewness, when using appropriate robust models and
hyperparameters. We further show that extending the optimization problem with a correlation penalty can notably reduce portfolio correlation with an arbitrary return sequence,
with only a small impact on other performance metrics.

## Robust Portfolio Selection Problems: A Comprehensive Review [arxiv](https://arxiv.org/abs/2103.13806)
Alireza Ghahtarani, Ahmed Saif, Alireza Ghasemi

In this paper, we provide a comprehensive review of recent advances in robust portfolio selection problems and their extensions, from both operational research and financial perspectives. A multi-dimensional classification of the models and methods proposed in the literature is presented, based on the types of financial problems, uncertainty sets, robust optimization approaches, and mathematical formulations. Several open questions and potential future research directions are identified.


## Generative Meta-Learning Robust Quality-Diversity Portfolio [link](https://arxiv.org/abs/2307.07811)
Kamer Ali Yuksel

This paper proposes a novel meta-learning approach to optimize a robust portfolio ensemble. The method uses a deep generative model to generate diverse and high-quality sub-portfolios combined to form the ensemble portfolio. The generative model consists of a convolutional layer, a stateful LSTM module, and a dense network. During training, the model takes a randomly sampled batch of Gaussian noise and outputs a population of solutions, which are then evaluated using the objective function of the problem. The weights of the model are updated using a gradient-based optimizer. The convolutional layer transforms the noise into a desired distribution in latent space, while the LSTM module adds dependence between generations. The dense network decodes the population of solutions. The proposed method balances maximizing the performance of the sub-portfolios with minimizing their maximum correlation, resulting in a robust ensemble portfolio against systematic shocks. The approach was effective in experiments where stochastic rewards were present. Moreover, the results (Fig. 1) demonstrated that the ensemble portfolio obtained by taking the average of the generated sub-portfolio weights was robust and generalized well. The proposed method can be applied to problems where diversity is desired among co-optimized solutions for a robust ensemble. The source-codes and the dataset are in the supplementary material.



## A Consistently oriented basis for eigenanalysis: improved directional statistics [link](https://link.springer.com/article/10.1007/s41060-024-00570-5)
Jay Damask

The algorithm derived in this article, which builds upon the original paper, takes a holistic view of the handedness of an orthonormal eigenvector matrix so as to transfer what would have been labeled as a reflection in the original algorithm into a rotation through a major arc in the new algorithm. In so doing, the angular wrap-around on the interval 
 that exists in the original is extended to a 
 interval for primary rotations, which in turn provides clean directional statistics. The modified algorithm is detailed in this article and an empirical example is shown. The empirical example is analyzed in the context of random matrix theory, after which two methods are discussed to stabilize eigenvector pointing directions as they evolve in time. The thucyd Python package and source code, reported in the original paper, has been updated to include the new algorithm and is freely available.

## The Economic Value of MSE [link](https://www.researchgate.net/publication/381196782_The_Economic_Value_of_Mean_Squared_Error_Evidence_from_Portfolio_Selection)
Zhaokun Cai et al

When designing and evaluating estimators, the mean squared error (MSE) is the most commonly
used generic statistical loss function because it captures the bias-variance tradeoff and allows
easy analytical and numerical treatment. However, MSE estimators are often applied to decision
problems for which the loss function is different, raising questions about how much value there
is in using a generic statistical loss function like the MSE rather than a decision loss function.
We elucidate this question through the lens of the portfolio selection problem by showing that
for several important portfolio rules, there is a positive linear relation between the MSE and
a portfolio-decision loss function. Moreover, shrinkage portfolio estimators derived under these
two loss functions are typically close to each other. Our findings highlight the economic value
of MSE to serve as a general-purpose statistical loss function in portfolio selection.



## Improved Portfolio Diversification Through Unsupervised Learning [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4580833)
Michael J. Lewis

From a theoretical perspective, portfolio optimization has been well understood for quite some time; Markowitz’ Critical Line Method stems from 1956, for example. In practice, the covariance matrix for portfolio returns is known to be noisy and frequently ill-conditioned, making the necessary inversion of the matrix impractical and inaccurate.

The approach of shrinking the covariance matrix in practice solves the inversion issue, but in doing so modifies the relationships between stocks, throwing the baby out with the bathwater. Hierarchical Risk Parity (HRP) took a novel approach to leverage these relationships, and in doing so sidestep the issue of inversion, but limited its scope to sorting the indices. We build upon this philosophy, introducing Recursive Clustering Risk Parity (RCRP). This procedure takes advantage of advances in unsupervised learning and inverse approximations to adhere more completely to these stock relationships by building and leveraging the corresponding tree structure to sidestep inversion, reduce noise impact, and in doing so enhance portfolio performance.

## Portfolio Optimization with Tracking-Error Constraints [pdf](https://merage.uci.edu/~jorion/papers/optim.pdf)
Philippe Jorion

This article explores the risk and return relationship of active portfolios subject to a constraint on tracking-error volatility (TEV), which can also be interpreted in terms of value at risk. Such a constrained portfolio is the typical setup for active managers who are given the task of beating a benchmark. The problem with this setup is that the portfolio manager pays no attention to total portfolio risk, which results in seriously inefficient portfolios unless some additional constraints are imposed. The development in this article shows that TEV-constrained portfolios are described by an ellipse on the traditional mean–variance plane. This finding yields a number of new insights. Because of the flat shape of this ellipse, adding a constraint on total portfolio volatility can substantially improve the performance of the active portfolio. In general, plan sponsors should concentrate on controlling total portfolio risk.

## Machine Learning Risk Models [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3308964)
Zura Kakushadze and Willie Yu

We give an explicit algorithm and source code for constructing risk models based on machine learning techniques. The resultant covariance matrices are not factor models. Based on empirical backtests, we compare the performance of these machine learning risk models to other constructions, including statistical risk models, risk models based on fundamental industry classifications, and also those utilizing multilevel clustering based industry classifications.


## Dictionary Learning-Based Denoising for Portfolio [pdf](https://2023.ic-dsp.org/wp-content/uploads/2023/05/DSP2023-43.pdf)
Sadik, Et-tolba, Nsiri

In the finance industry, real-world data are affected
by noise, which comes from several external sources. This makes
it challenging to select optimal portfolios for profitable investment
strategies. Therefore, noise removal (or denoising) has become
important for investors to create accurate investment models
that guarantee better returns. In this paper, we propose a novel
dictionary learning-based denoising approach for financial time
series. The transform matrix in dictionary learning is built by
training the noisy data with a K-singular value decomposition (KSVD) algorithm. We evaluated the effectiveness of the proposed
method using the 30 Fama French portfolio (FF30) as sample
data. Furthermore, the out-of-sample performance of the denoising approach is tested under a minimum-variance framework.
Empirical results prove that the proposed dictionary learningbased denoising method outperforms the other benchmarks in
terms of portfolio selection


## Regularized Tyler’s Scatter Estimator: Existence, Uniqueness, and Algorithms [pdf](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6879466)
Ying Sun and Daniel P. Palomar

This paper considers the regularized Tyler’s scatter
estimator for elliptical distributions, which has received considerable attention recently. Various types of shrinkage Tyler’s estimators have been proposed in the literature and proved work effectively in the “large small ” scenario. Nevertheless, the existence
and uniqueness properties of the estimators are not thoroughly
studied, and in certain cases the algorithms may fail to converge.
In this work, we provide a general result that analyzes the sufficient condition for the existence of a family of shrinkage Tyler’s
estimators, which quantitatively shows that regularization indeed
reduces the number of required samples for estimation and the
convergence of the algorithms for the estimators. For two specific
shrinkage Tyler’s estimators, we also proved that the condition is
necessary and the estimator is unique. Finally, we show that the
two estimators are actually equivalent. Numerical algorithms are
also derived based on the majorization-minimization framework,
under which the convergence is analyzed systematically.


## James–Stein for the leading eigenvector [pdf](https://www.pnas.org/doi/epdf/10.1073/pnas.2207046120)
Lisa Goldberg and Alec Kercheval

Recent research identifies and corrects bias, such as excess dispersion, in the leadingsample eigenvector of a factor-based covariance  matrix estimated  from  a high-dimension low sample size (HL) data set. We show that eigenvector bias can have asubstantial impact on variance-minimizing optimization in the HL regime, while bias in estimated eigenvalues may have little effect. We describe a data-driven eigenvector shrinkage estimator in the HL regime called “James–Stein for eigenvectors” (JSE) andits close relationship with the James–Stein (JS) estimator for a collection of averages.We show, both theoretically and with numerical experiments, that, for certain variance-minimizing problems of practical importance, efforts to correct eigenvalues have little value in comparison to the JSE correction of the leading eigenvector. When certain extra information is present, JSE is a consistent estimator of the leading eigenvector


##  Rotational invariant estimator for general noisy matrices [pdf](https://arxiv.org/pdf/1502.06736.pdf) [code](https://github.com/GGiecold/pyRMT/blob/main/pyRMT.py)
Joël Bun, Romain Allez, Jean-Philippe Bouchaud, Marc Potters

We investigate the problem of estimating a given real symmetric signal matrix C from a noisy observation matrix M in the limit of large dimension. We consider the case where the noisy measurement M comes either from an arbitrary additive or multiplicative rotational invariant perturbation. We establish, using the Replica method, the asymptotic global law estimate for three general classes of noisy matrices, significantly extending previously obtained results. We give exact results concerning the asymptotic deviations (called overlaps) of the perturbed eigenvectors away from the true ones, and we explain how to use these overlaps to "clean" the noisy eigenvalues of M. We provide some numerical checks for the different estimators proposed in this paper and we also make the connection with some well known results of Bayesian statistics


## Estimating covariance matrices for portfolio optimization [pdf](http://www.gcoqueret.com/files/Estim_cov.pdf)
GUILLAUME COQUERET AND VINCENT MILHAU

We compare twelve estimators of the covariance matrix: the sample covariance matrix, the identity
matrix, the constant-correlation estimator, three estimators derived from an explicit factor model, three obtained
from an implicit factor model, and three shrunk estimators. Following the literature, we conduct the comparison
by computing the volatility of estimated Minimum Variance portfolios. We do this in two frameworks: first, an
ideal situation where the true covariance matrix would be known, and second, a real-world situation where it
is unknown. In each of these two cases, we perform the tests with and without short-sales constraints, and we
assess the impact of the universe and sample sizes on the results. Our findings are in line with those of Ledoit
and Wolf (2003), in that we confirm that in the absence of short-sales constraints, shrunk estimators lead in
general to the lowest volatilities. With long-only constraints, however, their performance is similar to that of
principal component estimators. Moreover, the latter estimators tend to imply lower levels of turnover, which
is an important practical consideration.


## A Modified CTGAN-Plus-Features Based Method for Optimal Asset Allocation [pdf](https://arxiv.org/pdf/2302.02269)
José-Manuel Peña, Fernando Suárez, Omar Larré, Domingo Ramírez, Arturo Cifuentes

We propose a new approach to portfolio optimization that utilizes a unique combination of synthetic data generation and a CVaR-constraint. We formulate the portfolio optimization problem as an asset allocation problem in which each asset class is accessed through a passive (index) fund. The asset-class weights are determined by solving an optimization problem which includes a CVaR-constraint. The optimization is carried out by means of a Modified CTGAN algorithm which incorporates features (contextual information) and is used to generate synthetic return scenarios, which, in turn, are fed into the optimization engine. For contextual information we rely on several points along the U.S. Treasury yield curve. The merits of this approach are demonstrated with an example based on ten asset classes (covering stocks, bonds, and commodities) over a fourteen-and-half year period (January 2008-June 2022). We also show that the synthetic generation process is able to capture well the key characteristics of the original data, and the optimization scheme results in portfolios that exhibit satisfactory out-of-sample performance. We also show that this approach outperforms the conventional equal-weights (1/N) asset allocation strategy and other optimization formulations based on historical data only.

## Cross Asset Portfolios of Tradable Risk Premia Indices - Hierarchical Risk Parity - Enhancing Returns [link](https://www.scribd.com/document/466110701/Cross-Asset-Portfolios-of-Tradable-Risk-Premia-Indices-Hierarchical-Risk-Parity-Enhancing-Returns-pdf#)


## Adaptive Seriational Risk Parity and Other Extensions for Heuristic Portfolio Construction Using Machine Learning and Graph Theory [pdf](https://jfds.pm-research.com/content/iijjfds/early/2021/10/06/jfds.2021.1.078.full-text.pdf)
Peter Schwendner, Jochen Papenbrock, Markus Jaeger and Stephan Krügel

In this article, the authors present a conceptual framework named adaptive seriational risk parity (ASRP) to extend hierarchical risk parity (HRP) as an asset allocation heuristic. The first step of HRP (quasi-diagonalization), determining the hierarchy of assets, is required for the actual allocation done in the second step (recursive bisectioning). In the original HRP scheme, this hierarchy is found using single-linkage hierarchical clustering of the correlation matrix, which is a static tree-based method. The authors compare the performance of the standard HRP with other static and adaptive tree-based methods, as well as seriation-based methods that do not rely on trees. Seriation is a broader concept allowing reordering of the rows or columns of a matrix to best express similarities between the elements. Each discussed variation leads to a different time series reflecting portfolio performance using a 20-year backtest of a multi-asset futures universe. Unsupervised learningbased on these time-series creates a taxonomy that groups the strategies in high correspondence to the construction hierarchy of the various types of ASRP. Performance analysis of the variations shows that most of the static tree-based alternatives to HRP outperform the single-linkage clustering used in HRP on a risk-adjusted basis. Adaptive tree methods show mixed results, and most generic seriation-based approaches underperform.



## A Constrained Hierarchical Risk Parity Algorithm with Cluster-based Capital Allocation [pdf](https://www.fmx.nfkatzke.com/Projects/HRP.pdf)
Johann Pfitzinger, Nico Katzke 

Hierarchical Risk Parity (HRP) is a risk-based portfolio optimisation algorithm, which has been shown to generate diversified portfolios with robust out-of-sample properties without the need for a positive-definite return covariance matrix (Lopez de Prado 2016). The algorithm applies machine learning techniques to identify the underlying hierarchical correlation structure of the portfolio, allowing clusters of similar assets to compete for capital. The resulting allocation is both well-diversified over risk sources and intuitively appealing. This paper proposes a method of fully exploiting the information created by the clustering process, achieving enhanced out-of-sample risk and return characteristics. In addition, a practical approach to calculating HRP weights under box and group constraints is introduced. A comprehensive set of portfolio simulations over 6 equity universes demonstrates the appeal of the algorithm for portfolios consisting of 20 − 200 assets. HRP delivers highly diversified allocations with low volatility, low portfolio turnover and competitive performance metrics.


## A Clustering Algorithm for Correlation Quickest Hub Discovery Mixing Time Evolution and Random Matrix Theory
 [pdf](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4241975)
 Alejandro Rodriguez Dominguez

We present a geometric version of Quickest Change Detection (QCD) and Quickest Hub Discovery (QHD) tests in correlation structures that allows us to include and combine new information with distance metrics. The topic falls within the scope of sequential, nonparametric, high-dimensional QCD and QHD, from which state-of-the-art settings developed global and local summary statistics from asymptotic Random Matrix Theory (RMT) to detect changes in random matrix law. These settings work only for uncorrelated pre-change variables. With our geometric version of the tests via clustering, we can test the hypothesis that we can improve state-of-the-art settings for QHD, by combining QCD and QHD simultaneously, as well as including information about pre-change time-evolution in correlations. We can work with correlated pre-change variables and test if the time-evolution of correlation improves performance. We prove test consistency and design test hypothesis based on clustering performance. We apply this solution to financial time series correlations. Future developments on this topic are highly relevant in finance for Risk Management, Portfolio Management, and Market Shocks Forecasting which can save billions of dollars for the global economy. We introduce the Diversification Measure Distribution (DMD) for modeling the time-evolution of correlations as a function of individual variables which consists of a Dirichlet-Multinomial distribution from a distance matrix of rolling correlations with a threshold. Finally, we are able to verify all these hypotheses.



## Hierarchical Sensitivity Parity [pdf](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4110188)
Alejandro Rodriguez Dominguez

In this work we present a new framework for modelling portfolio dynamics and how to incorporate this information in the portfolio selection process. We define drivers for asset and portfolio dynamics, and their optimal selection. We introduce the new Commonality Principle, which gives a solution for the optimal selection of portfolio drivers as being the common drivers. Asset dynamics are modelled by PDEs and approximated with Neural Networks, and sensitivities of portfolio constituents with respect to portfolio common drivers are obtained via Automatic Adjoint Differentiation (AAD). Information of asset dynamics is incorporated via sensitivities into the portfolio selection process. Portfolio constituents are projected into a hypersurface, from a vector space formed by the returns of common drivers of the portfolio. The commonality principle allows for the necessary geometric link between the hyperplane formed by portfolio constituents in a traditional setup with no exogenous information, and the hypersurface formed by the vector space of common portfolio drivers, so that when portfolio constituents are projected into this hypersurface, the representations of idiosyncratic risks from the hyperplane are kept at most in this new subspace, while systematic risks representations are added via exogenous information as part of this common drivers vector space. We build a sensitivity matrix, which is a similarity matrix of the projections in this hypersurface, and can be used to optimize for diversification on both, idiosyncratic and systematic risks, which is not contemplated on the literature. Finally, we solve the convex optimization problem for optimal diversification by applying a hierarchical clustering to the sensitivity matrix, avoiding quadratic optimizers for the matrix properties, and we reach over-performance in all experiments with respect to all other out-of-sample methods.

## Asymmetric Autoencoders for Factor-Based Covariance Matrix Estimation [pdf](https://dl.acm.org/doi/pdf/10.1145/3533271.3561715)
Kevin Huynh, Gregor Lenhard

Estimating high dimensional covariance matrices for portfolio optimization is challenging because the number of parameters to be estimated grows quadratically in the number of assets. When the matrix dimension exceeds the sample size, the sample covariance matrix becomes singular. A possible solution is to impose a (latent) factor structure for the cross-section of asset returns as in the popular capital asset pricing model. Recent research suggests dimension reduction techniques to estimate the factors in a data-driven fashion. We present an asymmetric autoencoder neural network-based estimator that incorporates the factor structure in its architecture and jointly estimates the factors and their loadings. We test our method against well established dimension reduction techniques from the literature and compare them to observable factors as benchmark in an empirical experiment using stock returns of the past five decades. Results show that the proposed estimator is very competitive, as it significantly outperforms the benchmark across most scenarios. Analyzing the loadings, we find that the constructed factors are related to the stocks’ sector classification.
 


## Theoretically Motivated Data Augmentation and Regularization for Portfolio Construction [arxiv](https://arxiv.org/abs/2106.04114)
Liu Ziyin, Kentaro Minami, Kentaro Imajo

The task we consider is portfolio construction in a speculative market, a fundamental problem in modern finance. While various empirical works now exist to explore deep learning in finance, the theory side is almost non-existent. In this work, we focus on developing a theoretical framework for understanding the use of data augmentation for deep-learning-based approaches to quantitative finance. The proposed theory clarifies the role and necessity of data augmentation for finance; moreover, our theory implies that a simple algorithm of injecting a random noise of strength to the observed return rt is better than not injecting any noise and a few other financially irrelevant data augmentation techniques.


## Pessimistic Offline Policy Optimization [pdf](https://arxiv.org/abs/2012.13682)
Qiang He, Xinwen Hou

Offline reinforcement learning (RL) aims to optimize policy from large pre-recorded datasets without interaction with the environment. This setting offers the promise of utilizing diverse and static datasets to obtain policies without costly, risky, active exploration. However, commonly used off-policy deep RL methods perform poorly when facing arbitrary off-policy datasets. In this work, we show that there exists an estimation gap of value-based deep RL algorithms in the offline setting. To eliminate the estimation gap, we propose a novel offline RL algorithm that we term Pessimistic Offline Policy Optimization (POPO), which learns a pessimistic value function. To demonstrate the effectiveness of POPO, we perform experiments on various quality datasets. And we find that POPO performs surprisingly well and scales to tasks with high-dimensional state and action space, comparing or outperforming tested state-of-the-art offline RL algorithms on benchmark tasksl


## A Generalized Approach to Portfolio Optimization: Improving Performance by Constraining Portfolio Norms [pdf](https://www.semanticscholar.org/paper/A-Generalized-Approach-to-Portfolio-Optimization%3A-DeMiguel-Garlappi/0c684e0b00e090e064b614f87db321951cfc66ff)
Victor DeMiguel, Lorenzo Garlappi, R. Uppal

In this paper, we provide a general nonlinear programming framework for
identifying portfolios that have superior out-of-sample performance in the presence
of estimation error. This general framework relies on solving the traditional
minimum-variance problem but subject to the additional constraint that the
norm of the portfolio-weight vector be smaller than a given threshold.
We show that our general framework nests as special cases several wellknown
(shrinkage and constrained) approaches considered in the literature. We
also use our general framework to propose several new portfolio strategies that
we term partial minimum-variance portfolios. These portfolios are obtained by
applying the classical conjugate-gradient method to solve the minimum-variance
problem.
We compare empirically (in terms of portfolio variance, Sharpe ratio, and
turnover), the out-of-sample performance of the new portfolios to various wellknown
strategies across several datasets. We find that the norm-constrained
portfolios we propose outperform shortsale-constrained portfolio approaches,
shrinkage approaches, the 1/N portfolio, factor portfolios, and also other strategies
considered in the literature.

## Seriation and Matrix Reordering Methods: An Historical Overview [pdf](http://innar.com/Liiv_Seriation.pdf)
Innar Liiv

Seriation is an exploratory combinatorial data analysis technique to reorder objects into a sequence along a one-dimensional continuum so that it best reveals regularity and patterning among the whole series. Unsupervised learning, using seriation and matrix reordering, allows pattern discovery simultaneously at three information levels: local fragments of relationships, sets of organized local fragments of relationships, and an overall structural pattern. This paper presents an historical overview of seriation and matrix reordering methods, several applications from the following disciplines are included in the retrospective review: archaeology and anthropology; cartography, graphics, and information visualization; sociology and sociometry; psychology and psychometry; ecology; biology and bioinformatics; cellular manufacturing; and operations research.


## The Locally Gaussian Partial Correlation [pdf](https://arxiv.org/pdf/1909.09681)
Håkon Otneim, Dag Tjøstheim

It is well known that the dependence structure for jointly Gaussian variables can be fully captured using correlations, and that the conditional dependence structure in the same way can be described using partial correlations. The partial orrelation does not, however, characterize conditional dependence in many non-Gaussian populations. This paper introduces the local Gaussian partial correlation (LGPC), a new measure of conditional dependence. It is a local version of the partial correlation coefficient that characterizes conditional dependence in a large class of populations. It has some useful and novel properties besides: The LGPC reduces to the ordinary partial correlation for jointly normal variables, and it distinguishes between positive and negative conditional dependence. Furthermore, the LGPC can be used to study departures from conditional independence in specific parts of the distribution. We provide several examples of this, both simulated and real, and derive estimation theory under a local likelihood framework. Finally, we indicate how the LGPC can be used to construct a powerful test for conditional independence, which, again, can be used to detect Granger causality in time series.


## Measuring asymmetries in financial returns : an empirical investigation using local gaussian correlation [pdf](https://openaccess.nhh.no/nhh-xmlui/bitstream/handle/11250/166806/A12_13.pdf?sequence=1&isAllowed=y)
Støve, Bård; Tjøstheim, Dag

A number of studies have provided evidence that financial returns exhibit asymmetric dependence, such as increased dependence during bear markets, but there seems to be no agreement as to how such asymmetries should be measured. We introduce the use of a new measure of local dependence to study this asymmetry. The central idea of the new approach is to approximate an arbitrary bivariate return distribution by a family of Gaussian bivariate distributions. At each point of the return distribution there is a Gaussian distribution that gives a good approximation at that point. The correlation of the approximating Gaussian distribution is taken as the local correlation in that neighbourhood. The new measure does not suffer from the selection bias of the conditional correlation for Gaussian data, and is able to capture nonlinear dependence. Analyzing several financial returns from the US, UK, German and French markets, we confirm and are able to explicitly quantify the asymmetry. Finally, we discuss a risk management application, and point out a number of possible extensions.

## Portfolio Allocation under Asymmetric Dependence in Asset Returns using Local Gaussian Correlations [pdf](https://arxiv.org/pdf/2106.12425)
Sleire et al

It is well known that there are asymmetric dependence structures between financial returns. In this paper we use a new nonparametric measure of local dependence, the local Gaussian correlation, to improve portfolio allocation. We extend the classical mean-variance framework, and show that the portfolio optimization is straightforward using our new approach, only relying on a tuning parameter (the bandwidth). The new method is shown to outperform the equally weighted (1/N) portfolio and the classical Markowitz portfolio for monthly asset returns data.

## Beyond Risk-Based Portfolios: Balancing Performance and Risk Contributions in Asset Allocation [pdf](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2867936_code886365.pdf?abstractid=2819789&mirid=1&type=2)
Ardia, Boudt, Nguyen

In a risk-based portfolio, there is no explicit control for the performance per unit of risk taken. We propose a framework to evaluate the balance between risk and performance at both the portfolio and component level, and to tilt the risk-based portfolio weights towards a state in which the performance and risk contributions are aligned. The key innovation is the Performance/Risk Contribution Concentration (PRCC) measure, which is designed to be minimal when, for all portfolio components, the performance and risk contributions are perfectly aligned. We investigate the theoretical properties of this measure and show its usefulness to obtain the PRCC modified risk-based portfolio weights, that avoid excesses in terms of deviations between the performance and risk contributions of the portfolio components, while still being close to the benchmark risk-based portfolio in terms of weights and relative performance.


## A Fast Algorithm for Computing High-dimensional Risk Parity Portfolios [pdf](https://arxiv.org/pdf/1311.4057)
Théophile Griveau-Billion, Jean-Charles Richard, Thierry Roncalli

In this paper we propose a cyclical coordinate descent (CCD) algorithm for solving high dimensional risk parity problems. We show that this algorithm converges and is very fast even with large covariance matrices (n > 500). Comparison with existing algorithms also shows that it is one of the most efficient algorithms.



## Improved iterative methods for solving risk parity portfolio [paper](https://www.emerald.com/insight/content/doi/10.1108/JDQS-12-2021-0031/full/html)
Jaehyuk Choi, Rong Chen 

Risk parity, also known as equal risk contribution, has recently gained increasing attention as a portfolio allocation method. However, solving portfolio weights must resort to numerical methods as the analytic solution is not available. This study improves two existing iterative methods: the cyclical coordinate descent (CCD) and Newton methods. The authors enhance the CCD method by simplifying the formulation using a correlation matrix and imposing an additional rescaling step. The authors also suggest an improved initial guess inspired by the CCD method for the Newton method. Numerical experiments show that the improved CCD method performs the best and is approximately three times faster than the original CCD method, saving more than 40% of the iterations.


## Covariance matrix testing in high dimensions using random projections
Ayyala, Ghosh and Linder

Estimation and hypothesis tests for the covariance matrix in high dimensions is a challenging problem
as the traditional multivariate asymptotic theory is no longer valid. When the dimension is larger than
or increasing with the sample size, standard likelihood based tests for the covariance matrix have poor
performance. Existing high dimensional tests are either computationally expensive or have very weak
control of type I error. In this paper, we propose a test procedure, CRAMP, for testing hypotheses
involving one or more covariance matrices using random projections. Projecting the high dimensional
data randomly into lower dimensional subspaces alleviates of the curse of dimensionality, allowing for the
use of traditional multivariate tests. An extensive simulation study is performed to compare CRAMP
against asymptotics-based high dimensional test procedures. An application of the proposed method to
two gene expression data sets is presented


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


### Continuous Time Mean-Variance Portfolio Selection: A Reinforcement Learning Framework [pdf](https://arxiv.org/pdf/1904.11392)
Haoran Wang, Xun Yu Zhou

We approach the continuous-time mean-variance (MV) portfolio selection with reinforcement learning (RL). The problem is to achieve the best tradeoff between exploration and exploitation, and is formulated as an entropy-regularized, relaxed stochastic control problem. We prove that the optimal feedback policy for this problem must be Gaussian, with time-decaying variance. We then establish connections between the entropy-regularized MV and the classical MV, including the solvability equivalence and the convergence as exploration weighting parameter decays to zero. Finally, we prove a policy improvement theorem, based on which we devise an implementable RL algorithm. We find that our algorithm outperforms both an adaptive control based method and a deep neural networks based algorithm by a large margin in our simulations.

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

## Out of sample performance of Asset Allocation Strategies
Daniela Kolusheva

## Using out-of-sample errors in portfolio optimization [pdf](https://www.clsbe.lisboa.ucp.pt/system/files/assets/files/2016-paper-pedro-barroso.pdf)
Pedro Barroso

Portfolio optimization usually struggles in realistic out of sample contexts. I deconstruct this stylized fact comparing historical estimates of the inputs of portfolio
optimization with their subsequent out of sample counterparts. I confirm that historical estimates are often very imprecise guides of subsequent values but also
find this lack of persistence varies significantly across inputs and sets of assets.
Strikingly, the resulting estimation errors are not entirely random. They have predictable patterns and can be partially reduced using their own previous history. A
plain Markowitz optimization using corrected inputs performs quite well, out of
sample, namely outperforming the 1/N rule. Also the corrected covariance matrix
captures the risk of optimal portfolios much better than the historical one

## Risk Parity, Maximum Diversification, and Minimum Variance: An Analytic Perspective [pdf](https://www.hillsdaleinv.com/uploads/Risk_Parity%2C_Maximum_Diversification%2C_and_Minimum_Variance-_An_Analytic_Perspective.pdf)
Roger Clark, Harindra de Silva, Steven Thorley

In any event, the primary purpose of this study
is to provide general analytic solutions to risk-based
portfolios, not just another empirical back test. Further examination of the historical data in regards to
transaction costs and turnover, for example in Li, Sullivan, and Garcia-Feijoo [2013], may shed more light
on the exploitability of the low-risk anomaly.


## Risk Parity: Silver Bullet or a Bridge Too Far? [pdf](https://www.callan.com/uploads/2020/05/91d4bcabd3f4e687695022501ac62030/chapter-4-from-managing-multiasset-strategies-2018.pdf)
Gregory C. Allen

In this chapter, I evaluate the risk parity argument from a theoretical
standpoint using the modern portfolio theory (MPT) framework of
Markowitz (1952) and Tobin (1958). I then examine the historical
performance (both simulated and actual) of risk parity portfolios relative to traditional portfolios used by institutional investors. Finally,
I discuss the evolution of risk parity strategies and the prevalence of
their use by institutional investors

## The Risk in Risk Parity: A Factor Based Analysis of Asset-Based Risk Parity [via](https://www.researchgate.net/publication/256038119_The_Risk_in_Risk_Parity_A_Factor_Based_Analysis_of_Asset_Based_Risk_Parity)
Bhansali, David, Rennison et al

The risks embedded in asset-based risk parity portfolios are explored using a simple, economically motivated factor approach. We show that such an approach can substantially demystify and make explicit the drivers of returns for asset-based risk parity portfolios. The proposed framework can be used to assess the “true” parity in the underlying risk factor exposures for a given portfolio; it also allows investors to understand the active risks that a manager might be taking against his default risk parity position. Using a number of commercial risk parity portfolio returns, we find that traditional asset-based risk strategies, which are diversified in the asset space, can often be dominated by only one or two risk factors (equity and bond factors). In addition, these risk parity portfolios often exhibit very aggressive tactical allocations to the underlying factors, suggesting that active views on asset and/or factor are being expressed in many risk parity portfolios.

## Online Portfolio Selection: A Survey [pdf](https://arxiv.org/pdf/1212.2129)
Bin LI, Steven C. H. Hoi

Online portfolio selection is a fundamental problem in computational finance, which has been extensively studied across several research communities, including finance, statistics, artificial intelligence, machine learning, and data mining, etc. This article aims to provide a comprehensive survey and a structural understanding of published online portfolio selection techniques. From an online machine learning perspective, we first formulate online portfolio selection as a sequential decision problem, and then survey a variety of state-of-the-art approaches, which are grouped into several major categories, including benchmarks, "Follow-the-Winner" approaches, "Follow-the-Loser" approaches, "Pattern-Matching" based approaches, and "Meta-Learning Algorithms". In addition to the problem formulation and related algorithms, we also discuss the relationship of these algorithms with the Capital Growth theory in order to better understand the similarities and differences of their underlying trading ideas. This article aims to provide a timely and comprehensive survey for both machine learning and data mining researchers in academia and quantitative portfolio managers in the financial industry to help them understand the state-of-the-art and facilitate their research and practical applications. We also discuss some open issues and evaluate some emerging new trends for future research directions.

## What's the big deal about risk parity? [pdf](https://www.researchgate.net/profile/Robert-Ferguson-14/publication/312284109_What%27s_the_big_deal_about_Risk_Parity/links/5a8049d7aca272a73769d1c0/Whats-the-big-deal-about-Risk-Parity.pdf)
Anna Agapova, Robert Ferguson, Dean Leistikow, Danny Meidan

It is often argued in defense of Risk Parity portfolios that they maximize the
Sharpe ratio if their securities have identical Sharpe ratios and identical correlations. However, securities have neither identical Sharpe ratios nor this correlation structure. In realistic
markets, Risk Parity portfolios do not maximize the Sharpe ratio, do not minimize variance,
do not maximize the Information ratio, and do not have any other commonly sought optimal
property. So, what’s the big deal about Risk Parity?


## Hierarchical Sensitivity Parity [pdf](https://arxiv.org/pdf/2202.08921)
Alejandro Rodriguez

n this work we present a new framework for modelling portfolio dynamics and how to incorporate this information in the portfolio selection process. We define drivers for asset and portfolio dynamics, and their optimal selection. We introduce the new Commonality Principle, which gives a solution for the optimal selection of portfolio drivers as being the common drivers. Asset dynamics are modelled by PDEs and approximated with Neural Networks, and sensitivities of portfolio constituents with respect to portfolio common drivers are obtained via Automatic Adjoint Differentiation (AAD). Information of asset dynamics is incorporated via sensitivities into the portfolio selection process. Portfolio constituents are projected into a hypersurface, from a vector space formed by the returns of common drivers of the portfolio. The commonality principle allows for the necessary geometric link between the hyperplane formed by portfolio constituents in a traditional setup with no exogenous information, and the hypersurface formed by the vector space of common portfolio drivers, so that when portfolio constituents are projected into this hypersurface, the representations of idiosyncratic risks from the hyperplane are kept at most in this new subspace, while systematic risks representations are added via exogenous information as part of this common drivers vector space. We build a sensitivity matrix, which is a similarity matrix of the projections in this hypersurface, and can be used to optimize for diversification on both, idiosyncratic and systematic risks, which is not contemplated on the literature. Finally, we solve the convex optimization problem for optimal diversification by applying a hierarchical clustering to the sensitivity matrix, avoiding quadratic optimizers for the matrix properties, and we reach over-performance in all experiments with respect to all other out-of-sample methods.


## On the properties of equally-weighted risk contributions portfolios
Maillard, Roncalli and Teiletche

Minimum variance and equally-weighted portfolios have recently prompted
great interest both from academic researchers and market practitioners, as their
construction does not rely on expected average returns and is therefore assumed to be robust. In this paper, we consider a related approach, where the
risk contribution from each portfolio components is made equal, which maximizes diversication of risk (at least on an ex-ante basis). Roughly speaking,
the resulting portfolio is similar to a minimum variance portfolio subject to
a diversication constraint on the weights of its components. We derive the
theoretical properties of such a portfolio and show that its volatility is located
between those of minimum variance and equally-weighted portfolios. Empirical
applications conrm that ranking. All in all, equally-weighted risk contributions portfolios appear to be an attractive alternative to minimum variance
and equally-weighted portfolios and might be considered a good trade-o between those two approaches in terms of absolute level of risk, risk budgeting
and diversication.

## High Performance Cholesky and Symmetric Indefinite Factorizations with Applications [pdf](https://www.maths.ed.ac.uk/sites/default/files/atoms/files/hogg.pdf)
Jonathan David Hogg

The process of factorizing a symmetric matrix using the Cholesky (LLT) or indefinite (LDLT) factorization of A allows the efficient solution of systems Ax = b when A is symmetric. This
thesis describes the development of new serial and parallel techniques for this problem and
demonstrates them in the setting of interior point methods.
In serial, the effects of various scalings are reported, and a fast and robust mixed precision
sparse solver is developed. In parallel, DAG-driven dense and sparse factorizations are developed
for the positive definite case. These achieve performance comparable with other world-leading
implementations using a novel algorithm in the same family as those given by Buttari et al. for
the dense problem. Performance of these techniques in the context of an interior point method
is assessed.



## Improved iterative methods for solving risk parity portfolio [pdf](https://www.emerald.com/insight/content/doi/10.1108/JDQS-12-2021-0031/full/pdf?title=improved-iterative-methods-for-solving-risk-parity-portfolio)
Jaehyuk Choi and Rong Chen

Risk parity, also known as equal risk contribution, has recently gained increasing attention as a portfolio
allocation method. However, solving portfolio weights must resort to numerical methods as the analytic
solution is not available. This study improves two existing iterative methods: the cyclical coordinate descent
(CCD) and Newton methods. The authors enhance the CCD method by simplifying the formulation using a
correlation matrix and imposing an additional rescaling step. The authors also suggest an improved initial
guess inspired by the CCD method for the Newton method. Numerical experiments show that the improved
CCD method performs the best and is approximately three times faster than the original CCD method, saving
more than 40% of the iterations

## On the Risk of Out-of-Smaple Portfolio Performance [pdf](https://www.researchgate.net/publication/351942213_On_the_Risk_of_Out-of-Sample_Portfolio_Performance)
Nathan Lassance, Alterto Martin-Utrera, Majeed Simaan

We show that estimated mean-variance portfolios bear substantial out-of-sample utility risk in high-dimensional settings or when these portfolios exploit near-arbitrage opportunities. We propose a robustness measure that balances out-of-sample utility mean and volatility using our novel analytical characterization of out-of-sample utility risk. While individual portfolios do not offer maximal robust performance, portfolio combinations achieve the optimal tradeoff between out-of-sample utility mean and volatility and are more resilient to estimation errors. Our analysis of out-of-sample performance risk has implications for constructing and evaluating quantitative investment strategies and models of the stochastic discount factor.


## Fat Tailed Factors [pdf](https://arxiv.org/pdf/2011.13637)
Jan Rosenzweig

Standard, PCA-based factor analysis suffers from a number of well known problems due to the random nature of pairwise correlations of asset returns. We analyse an alternative based on ICA, where factors are identified based on their non-Gaussianity, instead of their variance. Generalizations of portfolio construction to the ICA framework leads to two semi-optimal portfolio construction methods: a fat-tailed portfolio, which maximises return per unit of non-Gaussianity, and the hybrid portfolio, which asymptotically reduces variance and non-Gaussianity in parallel. For fat-tailed portfolios, the portfolio weights scale like performance to the power of 1/3, as opposed to linear scaling of Kelly portfolios; such portfolio construction significantly reduces portfolio concentration, and the winner-takes-all problem inherent in Kelly portfolios. For hybrid portfolios, the variance is diversified at the same rate as Kelly PCA-based portfolios, but excess kurtosis is diversified much faster than in Kelly, at the rate of n−2 compared to Kelly portfolios' n−1 for increasing number of components n.


## Portfolio Optimization Rules beyond the Mean-Variance Approach [pdf](https://arxiv.org/pdf/2305.08530)
Maxime Markov, Vladimir Markov

In this paper, we revisit the relationship between investors' utility functions and portfolio allocation rules. We derive portfolio allocation rules for asymmetric Laplace distributed $ALD( \mu , \sigma , \kappa)$ returns and compare them with the mean-variance approach, which is based on Gaussian returns. We reveal that in the limit of small $\frac{\mu}{\sigma}$, the Markowitz contribution is accompanied by a skewness term. We also obtain the allocation rules when the expected return is a random normal variable in an average and worst-case scenarios, which allows us to take into account uncertainty of the predicted returns. An optimal worst-case scenario solution smoothly approximates between equal weights and minimum variance portfolio, presenting an attractive convex alternative to the risk parity portfolio. We address the issue of handling singular covariance matrices by imposing conditional independence structure on the precision matrix directly. Finally, utilizing a microscopic portfolio model with random drift and analytical expression for the expected utility function with log-normal distributed cross-sectional returns, we demonstrate the influence of model parameters on portfolio construction. This comprehensive approach enhances allocation weight stability, mitigates instabilities associated with the mean-variance approach, and can prove valuable for both short-term traders and long-term investors.

## Optimal portfolio allocation with uncertain covariance matrix [pdf](https://arxiv.org/pdf/2311.07478)
Maxime Markov, Vladimir Markov

In this paper, we explore the portfolio allocation problem involving an uncertain covariance matrix. We calculate the expected value of the Constant Absolute Risk Aversion (CARA) utility function, marginalized over a distribution of covariance matrices. We show that marginalization introduces a logarithmic dependence on risk, as opposed to the linear dependence assumed in the mean-variance approach. Additionally, it leads to a decrease in the allocation level for higher uncertainties. Our proposed method extends the mean-variance approach by considering the uncertainty associated with future covariance matrices and expected returns, which is important for practical applications.



## A FAST PARALLEL ALGORITHM FOR SELECTED INVERSION OF STRUCTURED SPARSE MATRICES WITH APPLICATION TO 2D ELECTRONIC STRUCTURE CALCULATIONS [pdf](https://sites.math.duke.edu/~jianfeng/paper/parallel.pdf)
LIN LIN, CHAO YANG, JIANFENG LU, LEXING YING, AND WEINAN E

An efficient parallel algorithm is presented and tested for computing selected components of H−1 where H has the structure of a Hamiltonian matrix of two-dimensional lattice models
with local interaction. Calculations of this type are useful for several applications, including electronic structure analysis of materials in which the diagonal elements of the Green’s functions are
needed. The algorithm proposed here is a direct method based on an LDLT factorization. The
elimination tree is used to organize the parallel algorithm. Synchronization overhead is reduced by
passing the data level by level along this tree using the technique of local buffers and relative indices.
The performance of the proposed parallel algorithm is analyzed by examining its load balance and
communication overhead, and is shown to exhibit an excellent weak scaling on a large-scale high
performance parallel machine with distributed memory.


