from precise.skaters.covariance.bufhuberfactory import buf_huber_d0_factory
from precise.skaters.covarianceutil.differencing import d1_factory


def buf_huber_pcov_d0_a1_b2_n50(y, s, k=1,e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=1.0, b=2.0, n_buffer=50, e=e)


def buf_huber_pcov_d0_a05_b2_n50(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=0.5, b=2.0, n_buffer=50, e=e)


def buf_huber_pcov_d0_a1_b5_n50(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=0.5, b=5.0, n_buffer=50, e=e)


def buf_huber_pcov_d0_a1_b2_n100(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=1.0, b=2.0, n_buffer=100, e=e)


def buf_huber_pcov_d0_a05_b2_n100(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=0.5, b=2.0, n_buffer=100, e=e)


def buf_huber_pcov_d0_a1_b5_n100(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=0.5, b=5.0, n_buffer=100, e=e)


def buf_huber_pcov_d0_a1_b2_n200(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=1.0, b=2.0, n_buffer=200, e=e)


def buf_huber_pcov_d0_a05_b2_n200(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=0.5, b=2.0, n_buffer=200, e=e)


def buf_huber_pcov_d0_a1_b5_n200(y, s, k=1, e=1):
    assert k==1
    return buf_huber_d0_factory(y=y,s=s,a=0.5, b=5.0, n_buffer=200, e=e)


BUF_HUBER_D0_COV_SKATERS = [buf_huber_pcov_d0_a1_b2_n50, buf_huber_pcov_d0_a05_b2_n50, buf_huber_pcov_d0_a1_b5_n50,
                            buf_huber_pcov_d0_a1_b2_n100, buf_huber_pcov_d0_a05_b2_n100, buf_huber_pcov_d0_a1_b5_n100,
                            buf_huber_pcov_d0_a1_b2_n200, buf_huber_pcov_d0_a05_b2_n200, buf_huber_pcov_d0_a1_b5_n200]


def buf_huber_pcov_d1_a1_b2_n50(y, s, k=1, e=1):
    return d1_factory(y=y,s=s,k=k,a=1.0, b=2.0, n_buffer=50, e=e)


def buf_huber_pcov_d1_a1_b2_n100(y, s, k=1, e=1):
    return d1_factory(y=y,s=s,k=k,a=1.0, b=2.0, n_buffer=100, e=e)


BUF_HUBER_D1_COV_SKATERS = [buf_huber_pcov_d1_a1_b2_n50, buf_huber_pcov_d1_a1_b2_n100]
