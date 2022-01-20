import random
import numpy as np
from precise.skaters.vectormean.buffermedianpre import med


def test_buffer_median():
    xs = np.random.randn(500, 100)
    xs[17, 1] = np.nan
    s = {}
    n_buffer = random.choice([1, 5, 100])
    for k, x in enumerate(xs):
        s = med(s=s, x=x, n_buffer=n_buffer)
        np_median = np.nanmedian(xs[max(0, k - n_buffer + 1):k + 1], axis=0)
        s_median = s['median']
        if not np.allclose(np_median, s_median, atol=1e-6):
            print('urgh')
            assert False


if __name__=='__main__':
    test_buffer_median()