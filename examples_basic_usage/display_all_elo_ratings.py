from pprint import pprint

# Show current ratings

if __name__=='__main__':
    from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
    pprint(elo_from_win_files())
