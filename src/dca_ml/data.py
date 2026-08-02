from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MONTHLY_FILE = PROCESSED_DIR / "martin_selected_30_monthly_production_normalized.csv"


NUMERIC_COLUMNS = [
    "month_on_production",
    "oil_bbl",
    "casinghead_gas_mcf",
    "boe",
    "interval_length_proxy_ft",
]


def load_monthly_production(path: Path = MONTHLY_FILE) -> pd.DataFrame:
    """Load normalized monthly production data with stable dtypes."""
    df = pd.read_csv(path, dtype={"api8": str, "lease_no": str, "district": str})
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["cycle_year_month"] = df["cycle_year_month"].astype(str)
    df = df.sort_values(["api8", "month_on_production"]).reset_index(drop=True)
    return df


def summarize_panel(df: pd.DataFrame) -> dict:
    """Return simple panel diagnostics for README/report checks."""
    return {
        "rows": int(len(df)),
        "wells": int(df["api8"].nunique()),
        "max_month_on_production": int(df["month_on_production"].max()),
        "full_cohort_months": int(
            df.groupby("month_on_production")["api8"].nunique().loc[
                lambda counts: counts == df["api8"].nunique()
            ].index.max()
        ),
        "zero_oil_months": int((df["oil_bbl"] == 0).sum()),
    }


def train_test_by_month(
    df: pd.DataFrame,
    train_end_month: int = 24,
    test_end_month: int = 33,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split by month-on-production to avoid using future months for training."""
    train = df[df["month_on_production"] <= train_end_month].copy()
    test = df[
        (df["month_on_production"] > train_end_month)
        & (df["month_on_production"] <= test_end_month)
    ].copy()
    return train, test
