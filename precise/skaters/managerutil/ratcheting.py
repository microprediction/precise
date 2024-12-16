
from precise.skaters.locationutil.vectorfunctions import normalize
import math
import numpy as np


def ratchet_portfolios(ys, w, w_lower, w_upper, min_dw=1e-6)->([float], dict):
    """

         Process a month of data (say) with ratcheting trading to upper and lower envelope


    :param ys:          num_days y num_assets  log returns
    :param w:           portfolio at start of period
    :param w_lower:
    :param w_upper:
    :param min_dw:
    :return:  w, stats
    """
    print('not tested')
    w_prev = np.array(w)
    ys = np.array(ys).tolist()
    stats = {'profit':list(),
             'volume':list()}
    for y in ys:
        w_grow = w_prev*np.exp(y)
        stats['profit'].append(math.log(np.sum(w_grow)))
        w_roll = normalize( w_grow )
        w_next = ratchet_portfolios( w = w_roll, w_lower=w_lower, w_upper=w_upper, min_dw=min_dw )
        l1_trading_dist = sum(np.abs(w_next-w_prev))
        stats['volume'].append(l1_trading_dist)
        w_prev = w_next
    return w_next, stats



def ratchet_trades(w, w_lower, w_upper, min_dw:float=1e-6)->[float]:
    """
         Given a current portfolio w, and upper and lower envelopes, this
         procedure will try to construct a list of allocation adjustments dw summing
         to zero that take w to a new portfolio w+dw that is closer to satisfying

                   w_lower <= w + dw <= w_upper

         The algorithms steps are as follows:

             1. Determine all envelope-restoring buys and sells
             2. Sort by decreasing size into two piles: potential buy and potential sell queues
             3. If total sell volume exceeds buy volume, pop a trade off the front of the buy queue (or conversely)
             4. At each step of a greedy loop, take from the buy queue if existing trades net short (or conversely)
             5. Once a trade list is created in this fashion, walk backwards and at the first opportunity,
                 reduce the size of one trade so that all net trading sums to zero

    :param w:             Current portfolio
    :param w_lower:       Lower envelope
    :param w_upper:       Upper envelope
    :param min_dw:        Minimum size of a reallocation
    :return: dw:          Trades that move w towards envelope
    """

    # Create a list of sell and buy opportunities (size, direction, ndx) in decreasing size
    sells = sorted(
        [[max(0, wi - wui), -1, i] for i, (wi, wui) in enumerate(zip(w, w_upper)) if (wi > wui + min_dw)],
        reverse=True)
    buys = sorted(
        [[max(0, wli - wi), 1, i] for i, (wi, wli) in enumerate(zip(w, w_lower)) if (wli - wi > min_dw)],
        reverse=True)

    buy_volume = sum([trade[0] for trade in buys])
    sell_volume = sum([trade[0] for trade in sells])
    if sell_volume > buy_volume:
        trades = [sells.pop(0)]
    elif buy_volume > sell_volume:
        trades = [buys.pop(0)]
    else:
        # We're already in the envelope
        return [0 for _ in w]

    # Walk down the queues and greedy balance buys and sells
    while True:
        net = sum([trade[0] * trade[1] for trade in trades])
        if (net > 0):
            # We have been net buyers thus far
            if len(sells) == 0:
                break
            else:
                trades.append(sells.pop(0))
        else:
            # We have been net sellers thus far
            if len(buys) ==0:
                break
            else:
                trades.append(buys.pop(0))

    # Walk back up and balance
    pos = len(trades)-1
    while True:
        tr = trades[pos]
        tr_dir = tr[1]
        if ((net > 0) and (tr_dir>0)) or ((net < 0) and (tr_dir<0)):
            trades[pos][0] = trades[pos][0] - abs(net)
            break
        else:
            pos = pos-1

    # Kill zero trades
    trades = [ tr for tr in trades if abs(tr[1])>1e-9 ]

    # Convert back to trades
    dw = [0 for _ in w ]
    for tr in trades:
        dw[tr[2]] = tr[0]*tr[1]
    return dw




if __name__=='__main__':
    w = [0.1, 0.2, 0.1, 0.05, 0.025, 0.1, 0.025, 0.3, 0.1]
    w_lower = [0.075]*len(w)
    w_upper = [0.125]*len(w)
    dw = ratchet_trades(w=w,w_lower=w_lower,w_upper=w_upper)



