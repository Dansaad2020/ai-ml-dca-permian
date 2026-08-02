from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# This is the normalized Martin County production file packaged with this repository.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "martin_selected_30_monthly_production_normalized.csv"

# DCA outputs will be saved inside the local project outputs folder.
OUTPUT_DIR = PROJECT_ROOT / "reports" / "dca_outputs"


def load_data() -> pd.DataFrame:
    """Load the production data and convert key columns to numeric values."""
    df = pd.read_csv(DATA_FILE, dtype={"api8": str, "lease_no": str, "district": str})

    numeric_columns = [
        "month_on_production",
        "oil_bbl",
        "casinghead_gas_mcf",
        "boe",
        "interval_length_proxy_ft",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df.sort_values(["api8", "month_on_production"]).reset_index(drop=True)


def build_median_curve(df: pd.DataFrame) -> pd.DataFrame:
    """Create a median oil type curve for the full-cohort window, months 1-33."""
    median_curve = (
        df[df["month_on_production"].between(1, 33)]
        .groupby("month_on_production", as_index=False)
        .agg(median_oil_bbl=("oil_bbl", "median"))
    )
    return median_curve


def fit_exponential_decline(
    curve: pd.DataFrame,
    month_column: str,
    rate_column: str,
    start_month: int = 2,
    end_month: int = 24,
) -> tuple[float, float, pd.DataFrame]:
    """Fit q(t) = qi * exp(-Di * t) using a straight-line fit in log space."""
    fit_data = curve[curve[month_column].between(start_month, end_month)].copy()
    fit_data = fit_data[fit_data[rate_column] > 0].copy()

    x = fit_data[month_column].to_numpy(dtype=float)
    y = fit_data[rate_column].to_numpy(dtype=float)

    slope, intercept = np.polyfit(x, np.log(y), 1)

    qi = float(np.exp(intercept))
    di = float(-slope)

    return qi, di, fit_data


def predict_exponential(months: np.ndarray, qi: float, di: float) -> np.ndarray:
    """Predict oil rate for each month using exponential decline."""
    months = np.asarray(months, dtype=float)
    return qi * np.exp(-di * months)


def print_train_test_summary(df: pd.DataFrame) -> None:
    """Print the same train/test split used for the first modeling release."""
    train = df[df["month_on_production"].between(1, 24)].copy()
    test = df[df["month_on_production"].between(25, 33)].copy()

    print("\n=== Train/Test Split ===")
    print(f"Training months: 1-24")
    print(f"Testing months: 25-33")
    print(f"Training rows: {len(train):,}")
    print(f"Testing rows: {len(test):,}")
    print(f"Training wells: {train['api8'].nunique():,}")
    print(f"Testing wells: {test['api8'].nunique():,}")


def plot_median_fit(median_curve: pd.DataFrame) -> None:
    """Save a plot comparing the actual median curve to the exponential fit."""
    plt.figure(figsize=(10, 6))
    plt.plot(
        median_curve["month_on_production"],
        median_curve["median_oil_bbl"],
        marker="o",
        label="Actual median oil",
    )
    plt.plot(
        median_curve["month_on_production"],
        median_curve["exp_fit_oil_bbl"],
        linestyle="--",
        label="Exponential fit",
    )
    plt.axvspan(1, 24, alpha=0.10, label="Training months")
    plt.axvspan(25, 33, alpha=0.10, label="Testing months")
    plt.title("Median Type Curve: Actual vs Exponential Decline")
    plt.xlabel("Month on Production")
    plt.ylabel("Oil Production (bbl/month)")
    plt.legend()
    plt.grid(True, alpha=0.30)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "median_exponential_decline_fit.png", dpi=150)
    plt.close()


def save_outputs(median_curve: pd.DataFrame, qi: float, di: float) -> pd.DataFrame:
    """Save the fitted curve and fitted parameter summary."""
    fit_summary = pd.DataFrame(
        [
            {
                "curve_name": "median_type_curve",
                "fit_start_month": 2,
                "fit_end_month": 24,
                "qi_bbl_per_month": qi,
                "di_per_month": di,
                "di_percent_per_month": di * 100,
            }
        ]
    )

    median_curve.to_csv(OUTPUT_DIR / "median_exponential_decline_curve.csv", index=False)
    fit_summary.to_csv(OUTPUT_DIR / "exponential_decline_fit_summary.csv", index=False)

    return fit_summary


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = load_data()
    print_train_test_summary(df)

    median_curve = build_median_curve(df)
    qi, di, fit_data = fit_exponential_decline(
        median_curve,
        month_column="month_on_production",
        rate_column="median_oil_bbl",
    )

    plot_months = np.arange(1, 34)
    median_curve["exp_fit_oil_bbl"] = predict_exponential(plot_months, qi, di)

    plot_median_fit(median_curve)
    fit_summary = save_outputs(median_curve, qi, di)

    print("\n=== Exponential Decline Fit: Median Type Curve ===")
    print(f"Fit months used: {int(fit_data['month_on_production'].min())}-"
          f"{int(fit_data['month_on_production'].max())}")
    print(f"Fitted qi: {qi:,.0f} bbl/month")
    print(f"Fitted Di: {di:.4f} per month")
    print(f"Fitted Di: {di * 100:.2f}% per month")

    print("\n=== Saved Outputs ===")
    print(OUTPUT_DIR / "median_exponential_decline_fit.png")
    print(OUTPUT_DIR / "median_exponential_decline_curve.csv")
    print(OUTPUT_DIR / "exponential_decline_fit_summary.csv")

    print("\n=== Fit Summary Table ===")
    print(fit_summary.to_string(index=False))


if __name__ == "__main__":
    main()
