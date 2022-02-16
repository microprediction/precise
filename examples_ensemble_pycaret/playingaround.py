
# Example based on https://www.analyticsvidhya.com/blog/2021/07/automl-using-pycaret-with-a-regression-use-case-ii/

if __name__=='__main__':
    try:
        import pycaret
        from pycaret.datasets import get_data
        from pycaret.regression import setup, compare_models, create_model, tune_model, predict_model
    except ImportError:
        print('You gotta pip install pycaret, friend')

    all_data = get_data('diamond', profile=False)

    holdout = all_data[-500:]

    data = all_data[:-500]

    exp_reg102 = setup(data=data, target='Price', session_id=123,
                       normalize=True, transformation=True, transform_target=True,
                       combine_rare_levels=True, rare_level_threshold=0.05,
                       remove_multicollinearity=True, multicollinearity_threshold=0.95,
                       bin_numeric_features=['Carat Weight'],
                       log_experiment=True, experiment_name='diamond1',html=False)
    print('done')


    shortlist = ['catboost','xgboost','lightgbm','rf']
    print('Creating')
    workin = dict()
    for nm in shortlist:
        try:
            model = create_model(nm)
            workin[nm]=model
        except Exception as e:
            print(str(e))
            print('sorry no dice for '+nm)

    tuned = dict( [ (nm, tune_model(w)) for n,w in workin.items() ])

    y_hats = list()
    for nm, tuned_model in tuned:
        y_hat = predict_model(estimator=tuned_model, data=holdout)
        y_hats.append(y_hat)


