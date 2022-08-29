from precise.skatervaluation.battleutil.interpretingelo import manager_regressor_frame
from precise.skatervaluation.battleutil.exampleelos import EXAMPLE_MANAGER_ELOS


def test_interpret_elos():
    elos = EXAMPLE_MANAGER_ELOS
    df = manager_regressor_frame(elos)
    print(df[:5])


if __name__=='__main__':
    elos = EXAMPLE_MANAGER_ELOS
    df = manager_regressor_frame(elos)
    from precise.whereami import BATTLE_RESULTS_DIR
    df.to_csv(BATTLE_RESULTS_DIR+'/example_manager_regressor_frame.csv', index=False)
