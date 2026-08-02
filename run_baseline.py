from pathlib import Path

import pandas as pd

from src.dca_ml.data import load_monthly_production, summarize_panel, train_test_by_month
from src.dca_ml.evaluation import regression_metrics
from src.dca_ml.features import modeling_frame
from src.dca_ml.models import gradient_boosting_model, random_forest_model


REPORTS = Path("reports")


def main() -> None:
    df = load_monthly_production()
    print("Panel summary:", summarize_panel(df))

    frame, features, target = modeling_frame(df)
    train, test = train_test_by_month(frame, train_end_month=24, test_end_month=33)

    results = []
    for name, model in {
        "random_forest": random_forest_model(),
        "gradient_boosting": gradient_boosting_model(),
    }.items():
        model.fit(train[features], train[target])
        predictions = model.predict(test[features])
        metrics = regression_metrics(test[target], predictions)
        results.append({"model": name, **metrics})

    # Humility baseline: next month equals the most recent actual oil rate.
    lag_predictions = test[f"{target}_lag_1"].to_numpy()
    results.append({"model": "last_observed_rate", **regression_metrics(test[target], lag_predictions)})

    REPORTS.mkdir(exist_ok=True)
    pd.DataFrame(results).sort_values("mae").to_csv(REPORTS / "baseline_metrics.csv", index=False)
    print(pd.DataFrame(results).sort_values("mae").to_string(index=False))


if __name__ == "__main__":
    main()
