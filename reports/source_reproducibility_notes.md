# Martin County Type-Curve Reproducibility Guide

## Scope

This workflow creates an availability-constrained 30-well Pioneer convenience cohort from public Railroad Commission of Texas data. It is not a representative population study or an independent reserves report.

## Required Inputs

Place the original RRC packages under `data/raw` using the existing package folders:

- `PDQ_DSV_Production Data Query`
- `Horizontal Drilling Permit`
- `Completion Information`

The current completion archive is incomplete: it contains only approximately January 1 through February 13/14 for each year from 2021 through 2026.

## Run Order

From the `permian_type_curve` folder, using the bundled workspace Python and Node runtimes:

1. `scripts/build_martin_candidates.py`
2. `scripts/extract_candidate_completions.py`
3. `scripts/select_cohort_extract_production.py`
4. `scripts/analyze_real_cohort.py`
5. `scripts/build_reproducibility_manifest.py`
6. `build_real_data_workbook.mjs`

## Principal Outputs

- `data/processed/martin_cohort_selection_log.csv`
- `data/processed/martin_selected_30_wells.csv`
- `data/processed/martin_selected_30_monthly_production_normalized.csv`
- `data/processed/martin_observed_type_curve.csv`
- `data/processed/martin_selected_30_well_summary.csv`
- `data/processed/martin_fitted_forecast.csv`
- `data/processed/input_manifest.csv`
- `data/processed/reproducibility_manifest.json`
- `outputs/SEM_Martin_County_30_Well_Real_Data_Type_Curve.xlsx`

## Core Rules

- Horizontal status is matched using the RRC horizontal-permit API.
- One-well leases are identified using unique API count by district and lease.
- Month on production is rebased to first positive oil or casinghead-gas month.
- Pre-positive reporting rows are excluded; subsequent zero-production months are retained.
- Observed P25/P50/P75 use inclusive linear percentiles.
- The oil decline fit uses observed P50 months 2-24.
- Month one is retained as an observed partial-month anchor.
- Oil transitions to a 0.8% monthly exponential terminal decline.
- Modeled oil is accumulated until the rate falls below 250 bbl/month.
- Gas forecast is suppressed pending resolution of its boundary-fit behavior.

## Required QA Checks

- Selected API values must be unique.
- District and lease keys must be unique across the final 30 wells.
- All 30 wells must have at least 18 normalized production months.
- The full cohort must remain present through month 33.
- Workbook formula-error scan must return zero matches.
- Dashboard values must reconcile to processed QC JSON.

## External-Use Boundary

Until full-year completion coverage is obtained, describe this as an availability-constrained convenience cohort. Do not claim it represents all Pioneer or Martin County wells. Do not describe the modeled oil result as economic-limit EUR.
