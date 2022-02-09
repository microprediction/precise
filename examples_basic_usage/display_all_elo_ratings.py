from pprint import pprint

# Show current ratings


def example():
    from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
    pprint(elo_from_win_files())


if __name__=='__main__':
    example()
