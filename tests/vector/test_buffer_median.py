
import numpy as np
from precise.skaters.location.buffermedianpre import med


def test_buffer_median():
    xs = np.random.randn(500, 100)
    xs[17, 1] = np.nan
    for n_buffer in [1,5,100]:
        x_seen = list()
        s = {}
        for k, x in enumerate(xs):
            x_seen.append(x)
            if len(x_seen)>n_buffer:
                x_seen.pop(0)
            s = med(s=s, x=x, n_buffer=n_buffer)
            np_median = np.nanmedian(x_seen, axis=0)
            s_median = s['median']
            if not np.allclose(np_median, s_median, atol=1e-6, equal_nan=True):
                print('urgh')
                assert False


if __name__=='__main__':
    test_buffer_median()