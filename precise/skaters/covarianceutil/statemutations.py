

def both_cov(s):
    """ Ensure tracking object has both population and sample cov """
    if s.get('n_samples')>1:
        if s.get('scov') is None and s['pcov'] is not None:
            s['scov'] = s['n_samples']/(s['n_samples']-1)*s['pcov']
        if s.get('pcov') is None and s['scov'] is not None:
            s['pcov'] = (s['n_samples'] - 1)/ s['n_samples'] * s['scov']
    return s
