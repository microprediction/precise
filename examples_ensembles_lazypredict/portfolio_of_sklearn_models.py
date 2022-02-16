
from sklearn import datasets
from sklearn.utils import shuffle
import numpy as np
from pprint import pprint
import time

# Construct a portfolio of models using lazypredict

# Train on X_train, y_train
# Select best based on X_test, y_test out of sample performance
# Retrain on X_train+X_test
# Estimate portfolio using X_test,y_test covariance
# Compare the val performance of:
# The best model from step 2, retrained in step 3.
# A weighted combination of models from step 4.


def manager_versus_best_model_avg(mgr=None):
    """
         Example of comparing manager to best model on an sklearn dataset
    """
    from precise.skaters.location.empirical import emp_d0
    s = {}
    while True:
        y = manager_versus_best_model(mgr=mgr, verbose=False)
        rmse_errors, y_cov, s = emp_d0(y=y,s=s,k=1)   # <-- Update running mean rmse estimates 
        
        print(' ')
        print(' ')
        rmse_comparison = dict(zip(['port','best'],rmse_errors))
        pprint(rmse_comparison)
        print(' ')
        time.sleep(1)


def manager_versus_best_model(mgr=None, verbose=True, n_train = 50, n_test = 50):
    try:
        from lazypredict.Supervised import LazyRegressor
    except ImportError:
        raise Exception('pip install lazypredict')
    if mgr is None:
        from precise.skaters.managers.ppomanagers import ppo_sk_glcv_pcov_d0_n100_t0_vol_long_manager as mgr

    boston = datasets.load_boston()
    X, y = shuffle(boston.data, boston.target)
    X = X.astype(np.float32)
    X_train, y_train = X[:n_train], y[:n_train]
    X_test, y_test = X[n_train:(n_train+n_test)], y[n_train:(n_train+n_test)]
    X_val, y_val = X[(n_train+n_test):], y[(n_train+n_test):]
    X_train_and_test = X[:(n_train+n_test)]
    y_train_and_test = y[:(n_train+n_test)]

    # Train on train, predict test
    reg1 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    models1, predictions1 = reg1.fit(np.copy(X_train), np.copy(X_test), np.copy(y_train), np.copy(y_test))
    if verbose:
        print(models1[:5])

    # Train on train+test, predict validation
    reg2 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    X_train_and_test_copy = np.copy(X_train_and_test)
    X_val_copy = np.copy(X_val)
    models2, predictions2 = reg2.fit(X_train_and_test_copy, X_val_copy, np.copy(y_train_and_test), np.copy(y_val))
    yhat_val = predictions2.values

    # In-sample performance on train
    reg3 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    models3, predictions3 = reg3.fit(np.copy(X_train), np.copy(X_train), np.copy(y_train), np.copy(y_train))

    # In-sample performance on train + test
    reg4 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    models4, predictions4 = reg4.fit(np.copy(X_train_and_test), np.copy(X_train_and_test), np.copy(y_train_and_test), np.copy(y_train_and_test))

    # Train on train, predict val
    reg5 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    models5, predictions5 = reg5.fit(np.copy(X_train), np.copy(X_val), np.copy(y_train), np.copy(y_val))


    best_model_1 = models1.index[0]  # <-- Best out of sample on test
    best_model_2 = models3.index[0]  # <-- Best in sample on train
    best_model_3 = models4.index[0]  # <-- Best in sample on train+test

    # Train cov on out of sample prediction errors
    if verbose:
        print('Creating portfolio ...')
    s = {}
    yhat_test = np.copy(predictions1.values)
    n_test = len(yhat_test)
    es = [-1]*(n_test-1)+[1]
    for y, y_target,e in zip(yhat_test, y_test,es):
        y_error = np.copy(y-y_target)
        w, s = mgr(s=s, y=y_error, e=e)

    w_dict = sorted([(wi,mi) for (wi,mi) in zip(w, models1.index) if wi>0], reverse=True)
    if verbose:
        pprint(w_dict)

    # Refit models using all the train+test data, and combine
    sum_w = sum(w)
    yhat_weighted = np.dot( yhat_val, w )
    predictions2['>> weighted portfolio of models '] = yhat_weighted
    predictions2['>> best model (' + best_model_1 + ') retrained '] = predictions2[best_model_1]
    try:
        predictions2['>> best model (' + best_model_1 + ') not retrained '] = predictions5[best_model_1]
    except:
        pass
    predictions2['>> best in sample i (' + best_model_2 + ')'] = predictions2[best_model_2]
    predictions2['>> best in sample ii (' + best_model_3 + ')'] = predictions2[best_model_3]

    val_errors = predictions2.copy()
    for col in predictions2.columns:
        val_errors[col] = predictions2[col] - y_val

    sq_errors = val_errors**2
    the_mean_errors = sq_errors.mean()
    if verbose:
        print(' ')
        print('Performance on validation set:')
        print(the_mean_errors.sort_values())
        print('done')
    else:
        print(the_mean_errors.sort_values()[:5])
    import math
    port_rmse = math.sqrt( the_mean_errors['>> weighted portfolio of models '])
    best_rmse = math.sqrt( the_mean_errors['>> best in sample i (' + best_model_2 + ')'])
    y = [port_rmse, best_rmse]
    return y



if __name__=='__main__':
    manager_versus_best_model_avg()






