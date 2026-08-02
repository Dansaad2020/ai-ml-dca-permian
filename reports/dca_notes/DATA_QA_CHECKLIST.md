# Data QA Checklist

Use this checklist before modeling.

## 1. Dataset Identity

- [ ] Confirm the file used is `martin_selected_30_monthly_production_normalized.csv`.
- [ ] Confirm this is from the SEM UT Dallas `permian_type_curve` project.
- [ ] Confirm the dataset is a Martin County, Texas public-data cohort.

## 2. Basic Counts

Expected values:

- Rows: 1,220
- Wells: 30
- Maximum month on production: 54
- Full cohort coverage through month 33
- Zero-oil months retained after first positive production: 95

Checks:

- [ ] Row count matches 1,220.
- [ ] Unique `api8` count matches 30.
- [ ] Maximum `month_on_production` is 54.
- [ ] Every month from 1 through 33 has 30 wells.
- [ ] Zero-oil months are not accidentally removed.

## 3. Field Checks

- [ ] `api8` is treated as an identifier, not a first-pass ML feature.
- [ ] `month_on_production` is numeric and starts at 1 for each well.
- [ ] `oil_bbl` is numeric and non-negative.
- [ ] `cycle_year_month` can be used for calendar ordering.
- [ ] `interval_length_proxy_ft` is present and numeric.

## 4. Modeling Boundary

Initial release:

- Training: months 1-24
- Testing: months 25-33

Checks:

- [ ] Training window does not include future test months.
- [ ] Lag and rolling features use only prior months.
- [ ] No feature directly leaks the target month's actual production.

## 5. Limitation Language

Use:

> availability-constrained convenience cohort

Avoid:

> representative Permian study

Avoid:

> independent reserves report

## 6. First Modeling Decision

Before moving to DCA, decide:

- [ ] Oil only for release 1.
- [ ] Gas excluded from release 1.
- [ ] Months 25-33 used as the first clean test window.
- [ ] Month 1 handled carefully because it may be a partial-month anchor.
