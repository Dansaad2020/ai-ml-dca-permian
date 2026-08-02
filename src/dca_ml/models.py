from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def random_forest_model(random_state: int = 42) -> RandomForestRegressor:
    return RandomForestRegressor(
        n_estimators=300,
        min_samples_leaf=3,
        random_state=random_state,
        n_jobs=1,
    )


def gradient_boosting_model(random_state: int = 42) -> Pipeline:
    return Pipeline(
        steps=[
            ("scale", StandardScaler()),
            (
                "model",
                GradientBoostingRegressor(
                    random_state=random_state,
                    n_estimators=250,
                    learning_rate=0.03,
                    max_depth=3,
                ),
            ),
        ]
    )
