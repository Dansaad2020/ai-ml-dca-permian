# Classical DCA vs ML Forecasting on a Public Permian Cohort

This project extends a prior public-data Permian type-curve study into a Python model-comparison workflow. It compares classical decline curve analysis (DCA) baselines with simple machine learning forecasts on a 30-well Martin County, Texas cohort.

The central question is not whether ML is impressive. The question is whether ML improves decision-useful forecasting when compared with domain-informed baselines, and whether its errors, bias, and uncertainty are understandable enough for technical decision-making.

## Why This Project

Reservoir forecasting and AI safety evaluation share a practical habit: models should be judged against outcomes, not vibes. This project uses a familiar reservoir forecasting problem to practice empirical model evaluation, calibration thinking, and honest communication of model limits.

## Current Scope

- Basin: Permian Basin, Midland Basin subset
- County: Martin County, Texas
- Operator cohort: Pioneer Natural Resources USA, Inc.
- Sample: 30 selected horizontal oil wells
- Data source: public Railroad Commission of Texas production, permit, wellbore, and completion data used in the prior SEM project
- Forecast target: monthly oil production
- Current modeling window: train through month 24, evaluate months 25-33 where the full 30-well cohort remains present

## Methods

Current baselines:

- Last observed oil rate
- Trailing 3-month oil average
- Trailing 6-month oil average
- Linear regression
- Random forest regression
- Gradient boosting regression

Classical DCA baselines:

- Median type-curve exponential decline
- Median type-curve hyperbolic decline
- Per-well exponential decline
- Per-well hyperbolic decline
- Per-well harmonic decline, in notebook workflow

Technical recovery / duration-style scenarios:

- DCA modeled oil through month 120
- Recursive ML modeled oil through month 120
- 30-well DCA vs ML technical recoverable oil comparison table

Evaluation:

- MAE
- RMSE
- sMAPE
- mean and median forecast bias
- horizon/month-specific error analysis

## Data Boundary

This is an availability-constrained convenience cohort, not a representative population study or reserves report. The prior QA review found that completion archive coverage was incomplete and that the cohort should not be described as representative of all Pioneer or Martin County wells.

The project is oil-focused. Gas forecasting is excluded from the first release because the prior gas decline fit reached a search-grid boundary and was suppressed from external use.

Technical recovery outputs in this repository are not SPE PRMS reserves estimates. No economic limit, abandonment cutoff, commerciality screen, ownership adjustment, or reserves-category assessment has been applied.

## Quick Start

```bash
pip install -r requirements.txt
python run_baseline.py
```

The baseline run writes:

```text
reports/baseline_metrics.csv
```

The first baseline run is intentionally conservative. On the initial month 25-33 test window, the last-observed-rate baseline outperformed the first random forest and gradient boosting models. This is treated as a finding, not a failure: the project is designed to compare ML against strong baselines rather than assume ML should win.

## DCA Workflow Checkpoint

The DCA learning notebooks are organized under:

```text
notebooks/dca_workflow/
```

Current notebook/script artifacts:

```text
01_data_understanding.ipynb
01_data_understanding.py
02_exponential_decline_dca.ipynb
02_exponential_decline_dca.py
03_hyperbolic_decline_dca.ipynb
03_hyperbolic_decline_dca.py
04_harmonic_decline_dca.ipynb
05_dca_model_comparison.ipynb
06_simple_ml_forecast_baselines.ipynb
06_simple_ml_forecast_baselines_manual.ipynb
07_fixed_origin_ml_vs_dca.ipynb
08_export_dca_comparison_ready.ipynb
09_ml_dca_forecast_diagnostic_plots.ipynb
10_dca_eur_duration_forecast.ipynb
11_ml_duration_forecast_scenarios.ipynb
12_dca_ml_technical_recovery_comparison.ipynb
```

Supporting DCA notes are saved under:

```text
reports/dca_notes/
```

Generated DCA outputs currently available on disk are saved under:

```text
reports/dca_outputs/
```

Generated ML and DCA-vs-ML comparison outputs are saved under:

```text
reports/ml_outputs/
```

The workflow now includes short-horizon validation notebooks, DCA comparison-ready exports, diagnostic plots, DCA technical recovery forecasts, recursive ML technical recovery scenarios, and a combined 30-well DCA-vs-ML technical recovery comparison.

Key comparison artifacts:

```text
reports/dca_outputs/dca_30_well_technical_recoverable_oil_table.csv
reports/ml_outputs/ml_30_well_technical_recoverable_oil_table.csv
reports/ml_outputs/dca_ml_30_well_technical_recovery_comparison.csv
reports/ml_outputs/dca_ml_technical_recovery_scenario_totals.csv
```

## Project Structure

```text
data/processed/       Reused processed cohort data from the SEM project
reports/              Metrics, figures, limitations, and source QA notes
reports/dca_notes/    DCA project notes and data understanding
reports/dca_outputs/  Saved DCA CSV and PNG outputs
reports/ml_outputs/   Saved ML metrics, diagnostics, and DCA-vs-ML comparison outputs
src/dca_ml/           Python modules for loading, features, DCA, ML, and evaluation
run_baseline.py       First runnable model-comparison workflow
```

## Next Steps

1. Review notebooks 10-12 in Jupyter and confirm the markdown narrative matches the final figures/tables.
2. Write a short final summary explaining where DCA and ML differ for short-horizon scoring versus technical recovery scenarios.
3. Keep the reserves caveat prominent: the technical recovery tables are modeled oil outputs, not SPE PRMS reserves.
4. Optionally add a lightweight release note or final report section around `reports/ml_outputs/dca_ml_30_well_technical_recovery_comparison.csv`.
