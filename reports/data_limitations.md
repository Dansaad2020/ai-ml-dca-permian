# Data Limitations

This project reuses processed outputs from a prior SEM UT Dallas portfolio project:

`SEM_JD_Market_Research_2026-06-17/portfolio/permian_type_curve`

The original workflow created a Martin County, Texas, Midland Basin cohort using public Railroad Commission of Texas data.

## Key Limitations

- The 30-well cohort is an availability-constrained convenience cohort.
- It should not be described as representative of all Pioneer wells or all Martin County wells.
- Completion archive coverage in the prior project was incomplete, covering approximately January 1 through February 13/14 for each year from 2021 through 2026.
- Texas production data is often lease-level. The prior workflow selected single-well leases to mitigate allocation ambiguity, but the project should still describe this assumption clearly.
- Gas forecasting is excluded from the first AI/ML release because the prior gas decline fit reached a boundary and was suppressed from external use.
- The first modeling comparison uses months 25-33 for testing because the full 30-well cohort is present through month 33.

## Safe External Description

Use:

> A Python model-comparison project using a 30-well Martin County public-data convenience cohort.

Avoid:

> A representative Permian population study.

Avoid:

> An independent reserves report.
