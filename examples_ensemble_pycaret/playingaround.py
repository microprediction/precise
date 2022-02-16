import numpy as np
import pandas as pd

# TODO: Illustrate the use of a portfolio manager applied to model residuals
# We use pycaret to generate some model predictions for various models
# Example based on https://www.analyticsvidhya.com/blog/2021/07/automl-using-pycaret-with-a-regression-use-case-ii/




if __name__=='__main__':
    try:
        import pycaret
        from pycaret.datasets import get_data
        from pycaret.regression import setup, compare_models, create_model, tune_model, predict_model
    except ImportError:
        print('You gotta pip install pycaret, friend')

    all_data = get_data('diamond', profile=False)

    n_train = 100
    n_test = 100
    all_data = all_data[:n_train+n_test]
    data = all_data[:n_train]
    holdout_data = all_data[n_train:]


    if True:
        # Is this needed?
        exp_reg102 = setup(data=all_data, target='Price', session_id=123,
                           normalize=True, transformation=True, transform_target=True,
                           combine_rare_levels=True, rare_level_threshold=0.05,
                           remove_multicollinearity=True, multicollinearity_threshold=0.95,
                           bin_numeric_features=['Carat Weight'],
                           log_experiment=True, experiment_name='diamond1',html=False)
        print('done')

    shortlist = ['catboost','xgboost','lightgbm','rf','et','ada','mlp','knn','huber','tr','llar','lar','ridge','lasso']
    print('Creating models and turning them')
    workin = dict()
    for nm in shortlist:
        try:
            model = create_model(nm)
            workin[nm]=model
            tune_model(workin[nm])
        except Exception as e:
            print(str(e))
            print('sorry no dice for '+nm)


    stuff = dict()
    for partition, the_data in zip(['train','holdout'],[data,holdout_data]):
        df = pd.DataFrame(columns=list(workin.keys()))
        for nm, tuned_model in workin.items():
            y_hat = predict_model(estimator=tuned_model, data=the_data)['Label']
            df[nm] = y_hat
        df.to_csv(partition+'.csv')
        stuff[partition] = y_hat

    # Use a portfolio manager to combine models ?
    ys = stuff['train'].values
    from precise.skaters.managers.schurmanagers import schur_weak_pm_t0_d0_r050_n25_g100_long_manager as mgr
    s = {}
    for y in ys:
        w, s = mgr(s=s,y=y)

    X = stuff['holdout'].values
    y_hat = np.dot(w, X)
    stuff['holdout']['blend'] = y_hat

    all_names = list(workin.keys())+['blend']
    holdout_error_df = pd.DataFrame(columns=all_names)
    for nm in all_names:
        holdout_error_df[nm] = (stuff['holdout'][nm]-holdout_data['Price'])**2

    print(holdout_error_df.describe())




