from precise.skaters.managers.equalmanagers import equal_long_manager as mgr
import numpy as np

def test_not_much():
    ys = np.random.randn(50,50)
    s = {}
    for y in ys:
        w, s = mgr(y=y,s=s,k=1,j=2,q=0.1)
