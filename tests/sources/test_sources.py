from precise.skatervaluation.battledata.sourceconventions import verify_source_outputs
from precise.skatervaluation.battledata.stockssource import stocks_source
from precise.skatervaluation.battledata.tmsource import tm_source
from precise.skatervaluation.battledata.m6source import m6_source
from precise.skatervaluation.battledata.allsources import params_category_and_data


def dont_test_m6_source_directly():
    verify_source_outputs(m6_source(params={'n_dim':5}))


def dont_test_m6_source_directly_no_etf():
    verify_source_outputs(m6_source(params={'etf':0,'n_dim':5}))


def dont_test_tm_source_directly():
    verify_source_outputs(tm_source(params={}))


def dont_test_tm_source_directly_noncollinear():
    verify_source_outputs(tm_source(params={'collinear':0}))


def dont_test_stocks_source_directly():
    verify_source_outputs(stocks_source(params={}))


def dont_test_tm_source_via_dispatch():
    verify_source_outputs(params_category_and_data(params={'topic':'tm'}))


def dont_test_stocks_source_via_dispatch():
    verify_source_outputs(params_category_and_data(params={'topic':'stocks'}))


def dont_test_m6_source_via_dispatch():
    verify_source_outputs(params_category_and_data(params={'topic':'m6','n_dim':5}))


if __name__=='__main__':
    dont_test_tm_source_directly_noncollinear()
    dont_test_stocks_source_directly()
    dont_test_tm_source_directly()
    dont_test_tm_source_via_dispatch()
    dont_test_tm_source_via_dispatch()
    dont_test_stocks_source_via_dispatch()
    dont_test_m6_source_via_dispatch()
    dont_test_m6_source_directly_no_etf

