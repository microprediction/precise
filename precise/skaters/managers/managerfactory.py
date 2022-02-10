

def static_cov_manager_factory_d0(y, s, f, port, f_kwargs:dict=None, port_kwargs:dict=None):
    """
       Basic manager pattern ignoring mean.
       Expects to receive changes in log(price)

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
             'port_state':{}}

    x_mean, x_cov, s['f_state'] = f(y=y,s=s['f_state'], k=1, **f_kwargs)
    w = port(cov=x_cov, **port_kwargs)
    return w, s

