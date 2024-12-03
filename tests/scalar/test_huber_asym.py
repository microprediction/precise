
import math


def huber_ratio(x):
    a = 0.2
    b = 1.0
    f = math.log(math.exp(a * x) + math.exp(-(a * x)) + b) / a
    c = math.log(2 + b) / a
    d = a / (2 + b)  # f-c ->  d y**2
    g = (f - c) / d  # g -> y**2
    h = x ** 2
    r = g / h
    return r


def test_huber_asym():
    # Quick test of the near zero asymptote
    assert abs(huber_ratio(x=0.0001)-1)<1e-2
