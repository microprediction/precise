from precise.skaters.portfoliostatic.equalport import equal_long_port


def static_cov_manager_factory_d0(y, s, f, port, e=1, f_kwargs:dict=None, port_kwargs:dict=None, n_cold=5):
    """
       Basic manager pattern ignoring mean.
       Expects to receive changes in log(price).
       If you have opinions on means, you'll have to incorporate them into variance somehow
       via the covariance skater. 

          :param f     cov skater ("d0")
          :param port  portfolio constructor

       :returns w, s
    """

    if f_kwargs is None:
        f_kwargs = {}
    if port_kwargs is None:
        port_kwargs = {}
    if not s:
        s = {'f_state':{},
             'port_state':{},
             'count':0}

    x_mean, x_cov, s['f_state'] = f(y=y,s=s['f_state'], k=1, e=e, **f_kwargs)
    s['count']+=1
    if s['count']>=n_cold and (e>0):
        w = port(cov=x_cov, **port_kwargs)
    else:
        w = equal_long_port(cov=x_cov)
    return w, s

