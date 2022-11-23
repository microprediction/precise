# Elo ratings
You have to run these notebooks. 

- [elo ratings for covariance](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb), or 
- [elo ratings for managers](https://github.com/microprediction/precise/blob/main/examples_basic_usage/compile_elo_ratings_for_managers.py)

as there is currently no automated production of Elo tables. 

### Remarks

I use Elo ratings, despite the shortcomings, because comparisions are extremely time intensive. Match results are recorded in hashed files for easy parallelization and avoidance of git merging. You can run the battle scripts if you like. See [these examples](https://github.com/microprediction/precise/tree/main/precise/skatervaluation/battlescripts/manager_var) for instance. To make a different battle you modify the name of the script and nothing else. Pull requests for match results are welcome, see below.

### Helping with Elo ratings
Sorry this isn't too streamlined, but if you'd like to perform some Elo calculations and share the results it is appreciated! 

    mkdir charity
    cd charity
    python3 -m venv charity
    source charity/bin/activate
    git clone https://github.com/microprediction/precise.git
    cd precise
    pip install -e . 
    python3 create_more_elo_ratings_thanks.py


-+-

Documentation [home](https://microprediction.github.io/precise)

View as [source](https://github.com/microprediction/precise/blob/master/docs/elo.md) or [web](https://microprediction.github.io/precise/elo)
