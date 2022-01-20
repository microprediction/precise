from heapq import heappush ,heappop, heapify ,_heapify_max
from typing import Union


# Running scalar median
# Ack: https://medium.com/mind-boggling-algorithms/streaming-algorithms-running-median-of-an-array-using-two-heaps-cd1b61b3c034


def med(s,x:Union[float,int]=None)->dict:
    """ Running median
       :param x: scalar float
    """
    if not s or s.get('low_heap') is None:
        s = dict()
        s['low_heap'] = []
        s['high_heap'] = []
        s['median'] = 0
    if x < s['median']:
        heappush(s['low_heap'], x)
        _heapify_max(s['low_heap'])
    else:
        heappush(s['high_heap'], x)

    if len(s['low_heap']) > len(s['high_heap'] ) +1:
        heappush(s['high_heap'], heappop(s['low_heap']))
        _heapify_max(s['low_heap'])
    elif len(s['high_heap']) > len(s['low_heap']) + 1:
        heappush(s['low_heap'], heappop(s['high_heap']))
        _heapify_max(s['low_heap'])

    if len(s['low_heap']) == len(s['high_heap']):
        s['median'] = float(s['low_heap'][0] + s['high_heap'][0] ) /2.0
    else:
        s['median'] = float(s['low_heap'][0]) if len(s['low_heap']) > len(s['high_heap']) else float(s['high_heap'][0])
    return s


if __name__=='__main__':
    import numpy as np
    import random
    xs = np.random.randn(random.choice([1,5,10,1000]))
    s = {}
    for x in xs:
        s = med(s=s,x=x)
    assert s['median'] == np.median(xs)
