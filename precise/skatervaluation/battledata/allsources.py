
from precise.skatervaluation.battledata.m6source import m6_source
from precise.skatervaluation.battledata.stockssource import stocks_source
from precise.skatervaluation.battledata.tmsource import tm_source
from precise.skatervaluation.battledata.sourceconventions import verify_source_outputs
import numpy as np

# Dispatch to data for Elo battles


SOURCES = [m6_source, stocks_source, tm_source]
SOURCE_NAMES = [ s.__name__.replace('_source','') for s in SOURCES ]


def params_category_and_data(params:dict)->(dict, str, np.ndarray):
    """
         Dispatcher for data sources suitable for Elo fights

         :param params  -  User or default parameters.
                        -  params['topic'] should be in SOURCE_NAMES
                        -  Other params can be specific to the data source
                        -  Most params are inferred from the battlescript file names

         :returns  (combined_params, category:str, xs:2d np array)
                        -  combined_params is a fleshed-out dictionary merging in some defaults
                        -  category refers to the battleresults directory
                        -  xs  is a collection of (typically) log differences
                                 o Each row is a sample
                                 o Each column is a variable

    """
    if params['topic']=='m6':
        outputs = m6_source(params=params)
    elif params['topic']=='stocks':
        outputs = stocks_source(params=params)
    elif params['topic']=='tm':
        outputs = tm_source(params=params)
    else:
        print('Available topics are '+ str(SOURCE_NAMES))
        print('Topic '+params.get('topic')+' not recognized.')
        raise ValueError()
    verify_source_outputs(outputs=outputs)
    return outputs

