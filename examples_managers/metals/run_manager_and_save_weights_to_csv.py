from precise.skaters.managers.schurmanagers import schur_diag_diag_ewa_r050_n25_s5_g100_long_manager as mgr
from precise.skatertools.data.preciousmetalsreturns import precious_metals_returns
import numpy as np
from precise.whereami import ROOT
import os

OUTPUT_CSV = os.path.join(ROOT,'private_examples','weights.csv')

if __name__=='__main__':
    ys = precious_metals_returns()
    ws = list()
    s = {}
    j = 20
    q = 1.0
    for y in ys:
        w, s = mgr(y=y,s=s,k=1,j=j,q=q)
        ws.append(w)

    ws = np.array(ws)
    print(np.shape(ws))
    ws.tofile(OUTPUT_CSV,sep=',')
    print('Saved to '+OUTPUT_CSV)

