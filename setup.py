import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="precise",
    version="0.3.1",
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
    packages=["precise","precise.z","precise.skaters",
              "precise.skaters.covariance","precise.skaters.covarianceutil",
               "precise.skaters.scalarutil",
              "precise.skaters.portfolio","precise.skaters.portfolioutil",
              "precise.skaters.location","precise.skaters.locationutil",
              "precise.skatertools",
              "precise.skatertools.comparison","precise.skatertools.data",
              "precise.skatertools.syntheticdata","precise.skatertools.visualization"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['numpy','momentum','kmeans1d','runthis','scikit-learn','osqp','pandas_datareader'],
    entry_points={
        "console_scripts": [
            "precise=precise.__main__:main",
        ]
    },
)
