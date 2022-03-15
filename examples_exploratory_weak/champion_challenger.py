# from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r01 as f
# from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r01_n100 as f
#from precise.skaters.covariance.ewalw import ewa_lw_scov_d0_r01 as f
from precise.skaters.covariance.ewaemp import ewa_emp_pcov_d0_r01 as f
from precise.skaters.portfoliostatic.unitport import unit_port
from precise.skaters.portfoliostatic.unitport import unit_port as champion_port
from precise.skaters.portfoliostatic.weakport import weak_long_port as challenger_port
from precise.skatertools.data.equityhistorical import random_cached_equity_dense
import numpy as np
from pprint import pprint
from precise.skaters.portfolioutil.portfunctions import negative_mass
from precise.skaters.covarianceutil.covdecomposition import random_portfolio_features

# A study to try to determine when and why one portfolio has better out of sample performance than another
import random
from precise.skaters.covarianceutil.covdecomposition import RANDOM_PORTFOLIO_FEATURE_NAMES


if __name__=='__main__':
    Ys = list()  # <-- realized portfolio variance
    Xs = list()  # <-- regressors
    include_neg_mass = False
    if include_neg_mass:
        Xnames = ['rel_norm', 'negative mass challenger', 'negative mass champion',
                  'negative mass unit'] + RANDOM_PORTFOLIO_FEATURE_NAMES
    else:
        Xnames = ['rel_norm'] + RANDOM_PORTFOLIO_FEATURE_NAMES
    Xn = [0 for n in Xnames]

    for iter in range(500):
        n_dim = random.choice([10, 25,40, 60,100,150, 200, 250])
        print('Iteration '+str(iter))
        ys = random_cached_equity_dense(n_obs=n_dim*2, n_dim=n_dim, k=1)
        s = {}

        w = np.ones(len(ys[0]))/len(ys[0])
        w_champion = np.copy(w)  # Keep lint happy
        w_challenger = np.copy(w)
        w_unit = np.copy(w)

        for ndx, y in enumerate(ys):
            if ndx>n_dim/2:
                champY = np.dot(w_champion, y) ** 2        # Realized portfolio variance
                challengeY = np.dot(w_challenger, y) ** 2  # Realized portfolio variance
                Yn = 1.0 if challengeY<champY else 0.0
                Ys.append(Yn)
                Xs.append(Xn)

            x, x_cov, s = f(y=y,s=s)
            w_challenger = challenger_port(cov=x_cov)
            w_champion = champion_port(cov=x_cov)

            # Some features
            d_mean = np.mean(np.diag(x_cov))
            try:
                n_mass_champion = negative_mass(w_champion)
            except np.linalg.LinAlgError:
                n_mass_champion = 0
            n_mass_challenger = negative_mass(w_challenger)
            w_unit = unit_port(x_cov)
            n_mass_unit = negative_mass(w_unit)
            try:
              rpf = random_portfolio_features(cov=x_cov, n_obs=11115)
            except:
              rpf = [ 0 for _ in RANDOM_PORTFOLIO_FEATURE_NAMES ]
            rel_norm = np.linalg.norm(w_champion) / np.linalg.norm(w_challenger)
            if include_neg_mass:
                Xnames = ['rel_norm', 'negative mass challenger', 'negative mass champion',
                          'negative mass unit'] + RANDOM_PORTFOLIO_FEATURE_NAMES
                Xn = [rel_norm, n_mass_challenger, n_mass_champion, n_mass_unit] + list(rpf)
            else:
                Xnames = ['rel_norm'] + RANDOM_PORTFOLIO_FEATURE_NAMES
                Xn = [n_mass_unit] + list(rpf)

        if len(Xs):
            from sklearn.preprocessing import StandardScaler
            from sklearn.linear_model import LinearRegression


            model = LinearRegression().fit(X=Xs, y=Ys)
            yHat = model.predict(Xs)
            reg_var = np.std(Xs, axis=0)
            importance = sorted(zip( reg_var*model.coef_, Xnames), reverse=True, key=lambda x: abs(x[0]) )


            pprint( {'model coef':model.coef_,
                     'champion better':np.mean(Ys),
                      'regressor std':np.std(Xs,axis=0),
                     'importance':importance})





    import matplotlib.pyplot as plt
    yHat = model.predict(Xs)
    plt.scatter(yHat,Ys)
    m, b = np.polyfit(yHat, Ys, 1)
    plt.plot(yHat, m * np.array(yHat) + b)
    plt.title('m=' + str(round(m, 4)) + ' b=' + str(round(b, 4)))
    plt.show()






and_the_results_are = {'champion better': 0.7318986918436386,
 'importance': [(0.033607355306393916, 'f2'),
                (-0.023353417369391703, 'f4'),
                (-0.013084663700970615, 'f3'),
                (0.007834184792080662, 'rel_norm'),
                (0.007210930958856752, 'f1'),
                (0.003323817072284449, 'f0'),
                (0.0027214866650434482, 'f6'),
                (0.0008564840210561352, 'f5')],
 'model coef': array([ 3.96006948e-06,  3.02359895e-02,  9.61353812e-02,  3.43625656e-01,
       -8.97719935e-02, -6.28447456e-02,  1.15690034e-02,  2.32852942e-02]),
 'regressor std': array([1.97829478e+03, 1.09929165e-01, 7.50080862e-02, 9.78022297e-02,
       1.45754407e-01, 3.71604931e-01, 7.40326539e-02, 1.16875769e-01])}


