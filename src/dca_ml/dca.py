import math

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def exponential_decline(t: np.ndarray, qi: float, decline: float) -> np.ndarray:
    return qi * np.exp(-decline * t)


def hyperbolic_decline(t: np.ndarray, qi: float, decline: float, b_factor: float) -> np.ndarray:
    return qi / np.power(1.0 + b_factor * decline * t, 1.0 / b_factor)


def fit_exponential(well_df: pd.DataFrame, target: str = "oil_bbl") -> dict:
    """Fit a simple exponential decline to one well's positive-rate history."""
    positive = well_df[well_df[target] > 0].sort_values("month_on_production")
    if len(positive) < 6:
        return {"status": "insufficient_history"}
    t = positive["month_on_production"].to_numpy(dtype=float) - positive["month_on_production"].min()
    y = positive[target].to_numpy(dtype=float)
    try:
        params, _ = curve_fit(
            exponential_decline,
            t,
            y,
            p0=[float(y[0]), 0.08],
            bounds=([1e-6, 0.0], [1e7, 2.0]),
            maxfev=10000,
        )
    except RuntimeError:
        return {"status": "fit_failed"}
    return {"status": "ok", "qi": float(params[0]), "decline": float(params[1])}


def predict_exponential(months: pd.Series, first_month: int, qi: float, decline: float) -> np.ndarray:
    t = months.to_numpy(dtype=float) - float(first_month)
    return exponential_decline(t, qi, decline)


def fit_hyperbolic_grid(type_curve: pd.DataFrame, rate_col: str = "p50_oil_bbl") -> dict:
    """Replicate the prior SEM-style grid search on the observed P50 type curve."""
    points = [
        (row["month_on_production"] - 2, float(row[rate_col]))
        for _, row in type_curve.iterrows()
        if 2 <= row["month_on_production"] <= 24 and float(row[rate_col]) > 0
    ]
    best = None
    for b_step in range(10, 27):
        b_factor = b_step * 0.05
        for decline_step in range(10, 61):
            decline = decline_step * 0.005
            log_qi = sum(
                math.log(rate) + math.log((1 + b_factor * decline * t) ** (1 / b_factor))
                for t, rate in points
            ) / len(points)
            qi = math.exp(log_qi)
            sse = sum(
                (
                    math.log(rate)
                    - math.log(qi / ((1 + b_factor * decline * t) ** (1 / b_factor)))
                )
                ** 2
                for t, rate in points
            )
            if best is None or sse < best["log_sse"]:
                best = {
                    "qi": qi,
                    "initial_monthly_decline": decline,
                    "b_factor": b_factor,
                    "log_sse": sse,
                    "fit_points": len(points),
                }
    return best
