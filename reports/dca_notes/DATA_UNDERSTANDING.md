# Data Understanding

## Source Dataset

Source project:

Prior SEM UT Dallas Permian type-curve project.

Primary file for this project:

`data/processed/martin_selected_30_monthly_production_normalized.csv`

This file contains normalized monthly production records for the selected Martin County cohort from the prior SEM UT Dallas project.

## Basic Shape

| Item | Value |
|---|---:|
| Rows | 1,220 |
| Wells | 30 |
| Maximum normalized month on production | 54 |
| Full cohort coverage | Through month 33 |
| Calendar range | 202201 to 202606 |
| Zero-oil months retained after first positive production | 95 |

## Initial Modeling Boundary

For the first modeling comparison, use:

- Training window: months 1-24
- Test window: months 25-33

Reason:

All 30 wells are present through month 33. After month 33, the cohort begins to shrink, so a first comparison that extends beyond month 33 would mix model error with sample attrition.

## Column Dictionary

| Column | Meaning | How We Use It |
|---|---|---|
| `api8` | 8-digit API identifier used as the well identifier in this processed cohort. | Group production by well. Do not use as a direct ML feature in the first model because it could encourage memorization. |
| `district` | RRC district. | Provenance and source context; not a first-pass model feature. |
| `lease_no` | RRC lease number. | Supports traceability and single-well lease logic from prior work. |
| `well_no` | Operator/RRC well number. | Human-readable well identity. |
| `lease_name` | Lease name. | Human-readable well/lease identity. |
| `operator_name` | Operator name. | Cohort context. Current cohort is Pioneer Natural Resources USA, Inc. |
| `field_name` | RRC field name. | Geological/field context. |
| `first_prod_month` | Reported first production month. | Source field; compare against normalized first positive production month. |
| `cycle_year_month` | Calendar production month in YYYYMM format. | Sort production chronologically and trace records to reporting months. |
| `month_on_production` | Normalized production month, rebased to first positive production. | Core time variable for DCA and ML forecasting. |
| `oil_bbl` | Monthly oil production in barrels. | Primary target variable for the first release. |
| `casinghead_gas_mcf` | Monthly casinghead gas production in thousand cubic feet. | Excluded from first release modeling; may be used later after gas-fit issues are addressed. |
| `boe` | Monthly barrels of oil equivalent. | Secondary context only for first release. |
| `interval_length_proxy_ft` | Proxy for completed interval/lateral length. | Candidate ML feature and cohort comparability variable. |
| `reported_first_month` | Original reported first production month preserved during normalization. | QA traceability. |
| `first_positive_prod_month` | First month with positive oil or casinghead gas. | Basis for normalized month-on-production. |
| `reported_month_on_production` | Original reported month-on-production before normalization. | QA traceability. |

## First Observations

1. Month 1 has lower total oil than month 2, likely reflecting partial first-month production effects.
2. The full cohort is available through month 33, making months 25-33 a clean first test period after training on months 1-24.
3. After month 33, well count drops from 30 to 27, then later to 14, so later months should be handled separately.
4. Zero-oil months are retained after first positive production. This is important because removing them could make the model unrealistically optimistic.
5. The dataset is suitable for an oil-focused DCA vs ML comparison, but not a representative population study.

## Questions To Answer Before Modeling

1. Should month 1 be included in DCA fitting, or treated as a partial-month anchor?
2. Should the first DCA fit be per-well, type-curve based, or both?
3. Should ML predict same-month oil using lag features, or explicitly predict one month ahead?
4. Should the first comparison use months 25-33 only, or also test alternative splits later?
5. Should gas be excluded entirely from release 1? Current recommendation: yes.

## Decisions For Release 1

Proposed:

- Use oil production as the target.
- Train first models on months 1-24.
- Test first models on months 25-33.
- Keep month 1 in exploratory plots but avoid relying on it alone for DCA fitting.
- Exclude `api8`, `lease_name`, and `well_no` from first ML features.
- Treat `interval_length_proxy_ft`, month-on-production, lagged oil, and rolling oil averages as first-pass features.
- Exclude gas forecasting from release 1.
