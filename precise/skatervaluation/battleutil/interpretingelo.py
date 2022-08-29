
import re
import pandas as pd
import numpy as np


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

    def infer_categorical_and_ordinal(elos):
        categorical = set()
        ordinal = set()
        for name, (_elo, _cpu) in elos:
            name = augment_alloc(name=name)
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

