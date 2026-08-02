import pandas as pd


def add_lag_features(df: pd.DataFrame, target: str = "oil_bbl") -> pd.DataFrame:
    """Create leakage-aware lag and rolling features for per-well forecasting."""
    out = df.sort_values(["api8", "month_on_production"]).copy()
    group = out.groupby("api8", group_keys=False)
    out[f"{target}_lag_1"] = group[target].shift(1)
    out[f"{target}_lag_2"] = group[target].shift(2)
    out[f"{target}_lag_3"] = group[target].shift(3)
    out[f"{target}_rolling_3"] = group[target].transform(
        lambda series: series.shift(1).rolling(3).mean()
    )
    return out


def modeling_frame(df: pd.DataFrame, target: str = "oil_bbl") -> tuple[pd.DataFrame, list[str], str]:
    """Return a model-ready frame and the baseline feature list."""
    out = add_lag_features(df, target=target)
    feature_columns = [
        "month_on_production",
        "interval_length_proxy_ft",
        f"{target}_lag_1",
        f"{target}_lag_2",
        f"{target}_lag_3",
        f"{target}_rolling_3",
    ]
    out = out.dropna(subset=feature_columns + [target]).copy()
    return out, feature_columns, target
