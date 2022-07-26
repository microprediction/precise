
def appeaser(x1, x2):
    """ Find the linear combination of two (net) portfolios that zeros out the largest coordinate """
    x1 = np.array(x1)
    x2 = np.array(x2)
    opposing = -np.sign(x1 * x2)
    j = np.argmax(abs(x1 - x2) * opposing)
    c1 = abs(x2[j])
    c2 = abs(x1[j])
    if max(opposing)>0.5 and (c1>0.01) and (c2>0.01):
        lambda1 = c1/(c1+c2)
        lambda2 = c2/(c2+c1)
        x = lambda1 * x1 + lambda2 * x2
        if abs(x[j])>1e-6:
            raise NotImplementedError('peter peter peter')
        return x
    else:
        return (x1+x2)/2


def appeasers(xs, n_max=20):
    origin = np.zeros_like(xs[0])
    xs_short = shortlist_by_l1_norm(origin=origin, xs=xs, n_max=n_max)
    x_long = list()
    for (x1,x2) in combinations(xs_short,2):
        a = appeaser(x1=x1,x2=x2)
        x_long.append(a)
    return x_long


def closest_appeaser_l1(w, ws, n_max=20, verbose=True):
    """ Extend the set of portfolios to include appeasers, then find the closest one in L1-norm
    :param w:
    :param ws:
    :param n_max:     Max number of portfolios used to create appeaser combinatiosn
    :param verbose:
    :return:
    """
    # Just an experiment. Doesn't really work too well.
    xs = [ np.array(wj)-np.array(w) for wj in ws]
    xs_appease = appeasers(xs=xs,  n_max=n_max)
    xs_all = xs + xs_appease
    ws_all = [ np.array(w) + xi for xi in xs_all]
    w_original = closest_point_l1(w=w,ws=ws)
    w_extended = closest_point_l1(w=w,ws=ws_all )
    is_same = np.linalg.norm(np.array(w_extended)-np.array(w_original))<1e-6
    if verbose:
        l1e = l1_distances(w=w, ws=ws_all)
        l1o = l1_distances(w=w, ws=ws)
        report = {'is_same':is_same,'max_o':max(l1o),'min_o':min(l1o),'min_e':min(l1e),'len_o':len(xs),'len_a':len(xs_appease),'e_save':(min(l1o)-min(l1e))}
        print(report)
    return w
