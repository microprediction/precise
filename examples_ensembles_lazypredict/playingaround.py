
from sklearn import datasets
from sklearn.utils import shuffle
import numpy as np
import pandas as pd
from pprint import pprint

if __name__=='__main__':
    try:
        from lazypredict.Supervised import LazyRegressor
    except ImportError:
        raise Exception('pip install lazypredict')

    boston = datasets.load_boston()
    X, y = shuffle(boston.data, boston.target)
    X = X.astype(np.float32)
    n_train = 100
    n_test = 50
    X_train, y_train = X[:n_train], y[:n_train]
    X_test, y_test = X[n_train:(n_train+n_test)], y[n_train:(n_train+n_test)]
    X_val, y_val = X[(n_train+n_test):], y[(n_train+n_test):]
    X_train_and_test = X[:(n_train+n_test)]
    y_train_and_test = y[:(n_train+n_test)]

    # Train on some
    reg1 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    models1, predictions1 = reg1.fit(np.copy(X_train), np.copy(X_test), np.copy(y_train), np.copy(y_test))
    print(models1[:5])

    # Train on some, predict validation
    reg2 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    X_train_and_test_copy = np.copy(X_train_and_test)
    X_val_copy = np.copy(X_val)
    models2, predictions2 = reg2.fit(X_train_and_test_copy, X_val_copy, np.copy(y_train_and_test), np.copy(y_val))
    yhat_val = predictions2.values
    print(models2[:5])

    # In-sample performance on train
    reg3 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    models3, predictions3 = reg3.fit(np.copy(X_train), np.copy(X_train), np.copy(y_train), np.copy(y_train))

    # In-sample performance on train + test
    reg4 = LazyRegressor(verbose=0, ignore_warnings=False, custom_metric=None, predictions=True)
    models4, predictions4 = reg4.fit(np.copy(X_train_and_test), np.copy(X_train_and_test), np.copy(y_train_and_test), np.copy(y_train_and_test))

    best_model_1 = models1.index[0]  # <-- Best out of sample on test
    best_model_2 = models3.index[0]  # <-- Best in sample on train
    best_model_3 = models4.index[0]  # <-- Best in sample on train+test

    if True:
        # Train cov on out of sample prediction errors
        print('Creating portfolio ...')
        from precise.skaters.managers.ppomanagers import ppo_sk_glcv_pcov_d0_n100_t0_vol_long_manager as mgr
        s = {}
        yhat_train = np.copy(predictions1.values)
        n_train = len(yhat_train)
        es = [-1]*(n_train-1)+[1]
        for y, y_target,e in zip(yhat_train, y_train,es):
            y_error = np.copy(y-y_target)
            w, s = mgr(s=s, y=y_error, e=e)

    else:
        n_models = len(models1)
        w = np.ones(n_models)/n_models

    w_dict = sorted(zip(w, models1.index), reverse=True)
    pprint(w_dict)

    # Refit models using all the train+test data, and combine

    sum_w = sum(w)
    yhat_weighted = np.dot( yhat_val, w )
    predictions2['weighted'] = yhat_weighted
    predictions2['best 1 (' + best_model_1 + ')'] = predictions2[best_model_1]
    predictions2['best 2 (' + best_model_2 + ')'] = predictions2[best_model_2]
    predictions2['best 3 (' + best_model_3 + ')'] = predictions2[best_model_3]

    val_errors = predictions2.copy()
    for col in predictions2.columns:
        val_errors[col] = predictions2[col] - y_val

    sq_errors = val_errors**2
    print(sq_errors.mean().sort_values())
    print('done')











