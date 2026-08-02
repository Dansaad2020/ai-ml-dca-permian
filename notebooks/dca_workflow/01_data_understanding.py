from pathlib import Path

import pandas as pd


# This is the processed production file packaged with this repository.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "martin_selected_30_monthly_production_normalized.csv"


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


def print_basic_summary(df: pd.DataFrame) -> None:
    """Print high-level facts about the dataset."""
    print("\n=== Basic Dataset Summary ===")
    print(f"Rows: {len(df):,}")
    print(f"Unique wells: {df['api8'].nunique():,}")
    print(f"Max month on production: {df['month_on_production'].max():.0f}")
    print(f"Calendar range: {df['cycle_year_month'].min()} to {df['cycle_year_month'].max()}")
    print(f"Zero-oil months retained: {(df['oil_bbl'] == 0).sum():,}")


def print_columns(df: pd.DataFrame) -> None:
    """Print the column names so we know what fields are available."""
    print("\n=== Columns ===")
    for column in df.columns:
        print(f"- {column}")


def print_sample_records(df: pd.DataFrame) -> None:
    """Show a few records for one well so the table becomes concrete."""
    print("\n=== First Five Records ===")
    sample_columns = [
        "api8",
        "lease_name",
        "cycle_year_month",
        "month_on_production",
        "oil_bbl",
        "casinghead_gas_mcf",
        "boe",
    ]
    print(df[sample_columns].head().to_string(index=False))


def monthly_coverage(df: pd.DataFrame) -> pd.DataFrame:
    """Count how many wells are present for each normalized production month."""
    coverage = (
        df.groupby("month_on_production")
        .agg(
            well_count=("api8", "nunique"),
            total_oil_bbl=("oil_bbl", "sum"),
            median_oil_bbl=("oil_bbl", "median"),
        )
        .reset_index()
        .sort_values("month_on_production")
    )
    return coverage


def print_coverage_summary(df: pd.DataFrame) -> None:
    """Print coverage by production month and identify the full-cohort window."""
    coverage = monthly_coverage(df)
    full_well_count = df["api8"].nunique()
    full_coverage = coverage[coverage["well_count"] == full_well_count]
    last_full_month = int(full_coverage["month_on_production"].max())

    print("\n=== Coverage By Month On Production ===")
    print(coverage.head(40).to_string(index=False))
    print(f"\nFull {full_well_count}-well cohort is present through month {last_full_month}.")


def print_well_summary(df: pd.DataFrame) -> None:
    """Summarize production history length and cumulative oil by well."""
    well_summary = (
        df.groupby("api8")
        .agg(
            rows=("api8", "size"),
            max_month=("month_on_production", "max"),
            first_cycle=("cycle_year_month", "min"),
            last_cycle=("cycle_year_month", "max"),
            cumulative_oil_bbl=("oil_bbl", "sum"),
        )
        .reset_index()
        .sort_values(["max_month", "api8"])
    )
    print("\n=== Well-Level Summary ===")
    print(well_summary.to_string(index=False))


def print_release_one_decision(df: pd.DataFrame) -> None:
    """State the first modeling window based on cohort coverage."""
    print("\n=== Release 1 Modeling Decision ===")
    print("Target: oil_bbl")
    print("Training months: 1-24")
    print("Testing months: 25-33")
    print("Reason: all 30 wells are present through month 33.")
    print("Gas forecasting: excluded from release 1.")
    print("Study type: model-comparison learning project, not a reserves report.")


def main() -> None:
    df = load_data()
    print_basic_summary(df)
    print_columns(df)
    print_sample_records(df)
    print_coverage_summary(df)
    print_well_summary(df)
    print_release_one_decision(df)


if __name__ == "__main__":
    main()
