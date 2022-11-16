try:
    from pypfopt import EfficientFrontier
    using_pyportfolioopt = True
except Exception:
    using_pyportfolioopt = False