
class KIsNotOne(Exception):
    pass


def raise_if_k_not_one(k):
    if not k in [1,None]:
        raise KIsNotOne('Skater only accepts k=1')

