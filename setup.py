import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="precise",
    version="0.16.7",
    description="The home of Schur Hierarchical Portfolios: an aesthetically pleasing version of Hierarchical Risk Parity",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/precise",
    author="microprediction",
    author_email="peter.cotton@microprediction.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["precise","precise.z",
              "precise.skaters",
              "precise.skaters.covariance",
              "precise.skaters.covarianceutil",
               "precise.skaters.scalarutil",
              "precise.skaters.portfoliostatic",
              "precise.skaters.portfolioutil",
              "precise.skaters.location",
              "precise.skaters.managers",
              "precise.skaters.managerutil",
              "precise.skaters.locationutil",
              "precise.inclusion",
              "precise.skatertools",
              "precise.skatertools.dictionaries",
              "precise.skatertools.data",
              "precise.skatertools.ensembling",
              "precise.skatertools.m6",
              "precise.skatertools.syntheticdata",
              "precise.skatervaluation",
              "precise.skatervaluation.covariancecomparisonutil",
              "precise.skatervaluation.managercomparisonutil",
              "precise.skatervaluation.portfoliocomparisonutil",
              "precise.skatervaluation.queues",
              "precise.skatervaluation.battleutil",
              "precise.skatervaluation.schurcomparisionutil",
              'precise.skatervaluation.battlescripts',
              'precise.skatervaluation.battlescriptscustom',
              "precise.skatervaluation.battlelatex",
              'precise.skatervaluation.battlescripts.cov_likelihood',
              'precise.skatervaluation.battlescripts.manager_info',
              "precise.skatervaluation.schurcomparisonutil",
              "precise.skatervaluation.schurcomparisionutil",
              'precise.skatervaluation.battlescripts.manager_var'
              ],
    test_suite='pytest',
    tests_require=['pytest','riskparityportfolio'],
    include_package_data=True,
    install_requires=['numpy','momentum>=0.2.7','kmeans1d','scikit-learn','latextable','tomark',
                      'pandas_datareader','pandas','scipy','pyportfolioopt','collinearity',
                      'yfinance','dictionaries'],
    entry_points={
        "console_scripts": [
            "precise=precise.__main__:main",
        ]
    },
)
