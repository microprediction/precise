
# Example based on https://www.analyticsvidhya.com/blog/2021/07/automl-using-pycaret-with-a-regression-use-case-ii/

if __name__=='__main__':
    try:
        import pycaret
        from pycaret.datasets import get_data
        from pycaret.regression import setup, compare_models, create_model, tune_model
    except ImportError:
        print('You gotta pip install pycaret, friend')

    dataset = get_data('diamond', profile=False)
    print(dataset)

    data = dataset.sample(frac=0.9, random_state=786)
    data_unseen = dataset.drop(data.index)
    data.reset_index(drop=True, inplace=True)
    data_unseen.reset_index(drop=True, inplace=True)
    print('Data for Modeling: ' + str(data.shape))
    print('Unseen Data For Predictions ' + str(data_unseen.shape))

    exp_reg102 = setup(data=data, target='Price', session_id=123,
                       normalize=True, transformation=True, transform_target=True,
                       combine_rare_levels=True, rare_level_threshold=0.05,
                       remove_multicollinearity=True, multicollinearity_threshold=0.95,
                       bin_numeric_features=['Carat Weight'],
                       log_experiment=True, experiment_name='diamond1',html=False)
    print('done')


    shortlist = ['catboost','xgboost','lightgbm','rf']
    print('Creating')
    for nm in shortlist:
        try:
            model = create_model(nm)
        except Exception as e:
            print(str(e))
            print('sorry no dice for '+nm)


    models = [ create_model(nm) for nm in shortlist ]
    print('Tuning')
    tuned = [ tune_model(m) for m in models ]
    print('')



