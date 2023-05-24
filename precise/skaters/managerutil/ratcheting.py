

def ratchet_trades(w, w_lower, w_upper, min_dw:float=1e-6)->[float]:
    """
         Given a current portfolio w, and upper and lower envelopes, this
         procedure will try to construct a list of allocation adjustments dw summing
         to zero that take w to a new portfolio w+dw that is closer to satisfying

                   w_lower <= w + dw <= w_upper

         The algorithm is somewhat heuristic but motivated by results suggesting a
         no-trade region for portfolios managed on a continuous basis in the presence of
         trading costs.


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

    if len(sells):
        trades = [sells.pop(0)]
    elif len(buys):
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



