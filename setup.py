import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="precise",
    version="0.1.0",
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
    packages=["precise","precise.oo","precise.covariance","precise.structure","precise.plotting",
              "precise.oo.empirical","precise.precision","precise.data","precise.synthetic"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=['numpy','momentum','kmeans1d','scikit-learn','osqp'],
    entry_points={
        "console_scripts": [
            "precise=precise.__main__:main",
        ]
    },
)
