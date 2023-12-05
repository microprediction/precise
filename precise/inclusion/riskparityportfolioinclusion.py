try:
    import riskparityportfolio
    using_riskparityportfolio = True
except Exception:
    using_riskparityportfolio = False



if __name__=='__main__':
    print(using_riskparityportfolio)