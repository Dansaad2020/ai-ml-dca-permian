# Notebooks

The main project notebooks are organized under:

```text
dca_workflow/
```

## Workflow Index

### Data Understanding and Classical DCA

1. `dca_workflow/01_data_understanding.ipynb`
2. `dca_workflow/02_exponential_decline_dca.ipynb`
3. `dca_workflow/03_hyperbolic_decline_dca.ipynb`
4. `dca_workflow/04_harmonic_decline_dca.ipynb`
5. `dca_workflow/05_dca_model_comparison.ipynb`

### ML Forecast Validation and DCA Comparison

6. `dca_workflow/06_simple_ml_forecast_baselines.ipynb`
7. `dca_workflow/06_simple_ml_forecast_baselines_manual.ipynb`
8. `dca_workflow/07_fixed_origin_ml_vs_dca.ipynb`
9. `dca_workflow/08_export_dca_comparison_ready.ipynb`
10. `dca_workflow/09_ml_dca_forecast_diagnostic_plots.ipynb`

### Technical Recovery / Duration-Style Scenarios

11. `dca_workflow/10_dca_eur_duration_forecast.ipynb`
12. `dca_workflow/11_ml_duration_forecast_scenarios.ipynb`
13. `dca_workflow/12_dca_ml_technical_recovery_comparison.ipynb`

The technical recovery notebooks produce modeled oil outputs through the stated forecast horizon. They are not SPE PRMS reserves estimates; no economic limit, abandonment cutoff, commerciality screen, ownership adjustment, or reserves-category assessment has been applied.

## Matching Python Helper Scripts

- `dca_workflow/01_data_understanding.py`
- `dca_workflow/02_exponential_decline_dca.py`
- `dca_workflow/03_hyperbolic_decline_dca.py`

## Key Output Locations

```text
reports/dca_outputs/
reports/ml_outputs/
```

Key comparison artifacts:

```text
reports/dca_outputs/dca_30_well_technical_recoverable_oil_table.csv
reports/ml_outputs/ml_30_well_technical_recoverable_oil_table.csv
reports/ml_outputs/dca_ml_30_well_technical_recovery_comparison.csv
reports/ml_outputs/dca_ml_technical_recovery_scenario_totals.csv
```
