from pprint import pprint

# Show current ratings


def show_em():
    from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
    pprint(elo_from_win_files(genre='cov_likelihood'))


if __name__=='__main__':
    show_em()
