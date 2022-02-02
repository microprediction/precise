
def normalize(x):
    ### See also portfolioutil.portfunctions.normalize_portfolio
    try:
        return x/sum(x)
    except (TypeError, ArithmeticError):
        try:
            return [xi/sum(x) for xi in x]
        except (TypeError, ArithmeticError):
            if sum(x)<1e-12:
                return x
            else:
                raise ValueError('??')
