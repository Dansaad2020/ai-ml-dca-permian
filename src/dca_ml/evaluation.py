import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def smape(y_true, y_pred) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    mask = denom > 0
    if not mask.any():
        return float("nan")
    return float(np.mean(np.abs(y_true[mask] - y_pred[mask]) / denom[mask]))


def regression_metrics(y_true, y_pred) -> dict:
    errors = np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float)
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "smape": smape(y_true, y_pred),
        "mean_bias": float(np.mean(errors)),
        "median_bias": float(np.median(errors)),
    }


def metrics_by_month(frame: pd.DataFrame, actual: str, predicted: str) -> pd.DataFrame:
    rows = []
    for month, group in frame.groupby("month_on_production"):
        metrics = regression_metrics(group[actual], group[predicted])
        rows.append({"month_on_production": month, **metrics, "n": len(group)})
    return pd.DataFrame(rows)
