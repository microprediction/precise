import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="precise",
    version="0.4.0",
    description="Online covariance and precision estimation",
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
              "precise.skaters.portfolio",
              "precise.skaters.portfoliostatic",
              "precise.skaters.portfolioutil",
              "precise.skaters.location",
              "precise.skaters.locationutil",
              "precise.skatertools",
              "precise.skatertools.components",
              "precise.skatertools.data",
              "precise.skatertools.ensembling",
              "precise.skatertools.m6",
              "precise.skatertools.syntheticdata",
              "precise.skatertools.visualization",
              "precise.skatervaluation",
              "precise.skatervaluation.queues",
              "precise.skatervaluation.battleutil",
              'precise.skatervaluation.battlescripts',
              'precise.skatervaluation.battlescripts.likelihood'],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['numpy','momentum>=0.2.5','kmeans1d','runthis','scikit-learn','osqp',
                      'pandas_datareader','seriate','pandas','scipy','pyportfolioopt'],
    entry_points={
        "console_scripts": [
            "precise=precise.__main__:main",
        ]
    },
)
