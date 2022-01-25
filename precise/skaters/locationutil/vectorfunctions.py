
def normalize(x):
    try:
        return x/sum(x)
    except TypeError:
        return [xi/sum(x) for xi in x]