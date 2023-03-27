
import re
import pandas as pd
import numpy as np


def gamma_plot(ratings, model_sub_string:str, min_gamma=0, max_gamma=100, lmbda=1):
    """ Plots the relationship between choice of gamma and Elo rating

        :ratings - The output from elo_from_win_files(genre=GENRE, category=CATEGORY_MATCH)

    """

    # Plot gamma relationship to Elo
    from matplotlib.pyplot import cm
    import numpy as np
    rainbow = cm.rainbow(np.linspace(0, 1, len(ratings)))
    from sklearn.linear_model import LinearRegression

    import matplotlib.pyplot as plt
    for category_and_ratings, c in zip(ratings, rainbow):
        category = category_and_ratings[0]
        elos = list()
        gammas = list()
        colors = list()
        for name, (elo,cpu) in category_and_ratings[1].items():
           if model_sub_string in name:
              gstr = name.split('_')[8]
              g = int(gstr[1:])
              if min_gamma <= g <= max_gamma:
                  elos.append(elo)
                  gammas.append(g)
                  colors.append(c)
        cat_splt = category.split('_')
        label = cat_splt[3]
        title = ' '.join( cat_splt[0:2] ) + cat_splt[-1]

        if max_gamma<100 and False:
            # Line of best fit
            X, Y = np.array(gammas).reshape(-1, 1), np.array(elos).reshape(-1, 1)
            plt.plot(X, LinearRegression().fit(X, Y).predict(X), color=c, linestyle='dashed')
        elif False:
            # Smooth fit
            import smoothfit
            a, b, n_knot = 0, 100, 99
            basis, coef = smoothfit.fit1d(x0=gammas, y0=elos, a=a, b=b, n=n_knot, lmbda=lmbda)
            plt.plot(basis.mesh.p[0], coef[basis.nodal_dofs[0]], linestyle='dashed', color=c)

        plt.scatter(x=gammas, y=elos, c=colors, label=label)


    plt.title('Gamma v. Elo (dimension p)')
    plt.xlabel('Gamma')
    plt.legend(loc='lower center')
    plt.ylabel('Elo')
    plt.grid();
    plt.show()



def manager_regressor_frame(elos):
    """
       Construct a dataframe where regressors are inferred from manager names.
    """
    MODEL_KEY_REPLACEMENTS = {'gamma': 'g','t0':'tzero'}
    MODEL_KEYS_NOT_USED = ['manager', 'manger', 'long', 'pcov', 'check']

    def augment_alloc(name):
        # Differentiate between 2nd and 3rd hints (usually alloc verus portfolio method)
        splt = name.split('_')
        if splt[2] == splt[1]:
            splt[2] = splt[2] + 'xx'  # Allocation
            splt[1] = splt[1] + 'xy'  # Portfolio
        return '_'.join(splt)

    def augment_weak(name):
        splt = name.split('_')
        if splt[0]=='weak':
            splt[0]='weakxz'
        return '_'.join(splt)

    def infer_categorical_and_ordinal(elos):
        categorical = set()
        ordinal = set()
        for name, (_elo, _cpu) in elos:
            name = augment_alloc(name=name)
            name = augment_weak(name=name)
            name_words = name.split('_')
            for wd in name_words:
                for r_old, r_new in MODEL_KEY_REPLACEMENTS.items():
                    wd = wd.replace(r_old, r_new)
                wd_head = re.search("[^\d]*", wd).group()
                if wd == wd_head:
                    if wd not in MODEL_KEYS_NOT_USED:
                        categorical.add(wd_head)
                else:
                    ordinal.add(wd_head)
        return categorical, ordinal

    def make_model_regs_elo(elos, categorical, ordinal):
        model_reg_elo = list()
        for name, (elo,cpu) in elos:
            name = augment_alloc(name=name)
            name = augment_weak(name=name)
            name_words = name.split('_')
            reg_pairs = list()
            for wd in list(set(name_words)):
                for r_old,r_new in MODEL_KEY_REPLACEMENTS.items():
                    wd = wd.replace(r_old,r_new)

                if wd in categorical:
                    pair = (wd+'_hot',1)
                else:
                    wd_head = re.search("[^\d]*", wd).group()
                    if wd_head in categorical:
                        pair = (wd+'_hot',1)
                    elif wd_head in ordinal:
                        wd_tail = wd[len(wd_head):]
                        pair = (wd_head+'_ord',float(wd_tail))
                    else:
                        pair = None
                if pair is not None:
                    reg_pairs.append(pair)
            model_reg_elo.append( (name, reg_pairs, elo) )
        return model_reg_elo

    def model_regs_elo_keys(model_regs_elo):
        kys = set()
        for model, regs, _elo in model_regs_elo:
            for k, v in regs:
                kys.add(k)
        return kys

    def model_regs_elo_to_frame(model_regs_elo):
        """
            Convert tuples into dataframe setting non-ordinal variables to 0.0
        """
        kys = model_regs_elo_keys(model_regs_elo)

        rows = list()
        for model, regs, elo in model_regs_elo:
            row_dict = dict([(k, np.nan if '_ord' in k else 0.0) for k in kys])
            row_dict.update({'elo': elo})
            for reg, val in regs:
                row_dict[reg] = val
            row = pd.DataFrame.from_dict(row_dict, orient='index').transpose()
            rows.append(row)
        df = pd.concat(rows)
        return df

    categorical, ordinal = infer_categorical_and_ordinal(elos)
    models_and_regs = make_model_regs_elo(elos=elos, categorical=categorical, ordinal=ordinal)
    df = model_regs_elo_to_frame(model_regs_elo=models_and_regs)
    return df

