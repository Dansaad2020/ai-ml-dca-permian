# Independent QA/QC and Judge Review

Date: June 19, 2026

Artifact: `outputs/SEM_Martin_County_30_Well_Real_Data_Type_Curve.xlsx`

## Verdict

**CONDITIONAL PASS**

The numerical construction, normalization, percentile calculations, oil decline fit, workbook formulas, and presentation are internally consistent. The artifact is not ready for external release until the cohort-coverage limitation and recovery-labeling issue are corrected.

## Release Blockers

### 1. Partial completion-archive coverage

The available completion archives cover only approximately January 1 through February 13/14 for each year from 2021 through 2026. Approved-completion availability was then used as an eligibility gate.

Consequences:

- Only 193 of 854 candidate APIs had an approved packet match.
- The 34-well comparable pool is partly a function of archive availability.
- The final 30 wells cannot be described as representative of the full Pioneer Martin County population.
- An independent sensitivity found 11 otherwise comparable submitted-packet wells; five could displace approved-packet wells under the same interval-distance ranking.

Required resolution:

- Preferred: acquire complete completion coverage and rerun selection.
- Alternative: use approved status as a QC flag rather than an eligibility gate, publish an approved-only versus all-usable-packet sensitivity, and label the result as a convenience cohort selected from available packets.

### 2. Fitted recovery is forecast-life limited, not cutoff limited

The fitted oil rate at month 240 is approximately 252.12 bbl/month, above the stated 250 bbl/month cutoff. Month 241 is approximately 250.11 bbl/month and month 242 is below cutoff.

Consequences:

- 433,446 bbl is 240-month modeled cumulative oil, not cutoff-defined EUR.
- Extending through the last month above the rate cutoff gives approximately 433,696 bbl.
- The numerical difference is immaterial, but the reserves terminology is material.
- A 250 bbl/month rate threshold is not an economic limit without prices, operating costs, taxes, water handling, and abandonment assumptions.

Required resolution:

- Rename the KPI to `20-Year Modeled Oil` or extend the forecast through the rate cutoff.
- Describe the threshold as a rate cutoff, not an economic limit.
- Do not describe the result as a proven median-well EUR.

## Additional Findings

1. The acquisition log specifies a 2022-2024 window, while final selection uses 2022-2023. Reconcile the written scope.
2. FracFocus is listed in the planned join logic but was not used. Either complete that join or mark it as a future enhancement.
3. The gas fit lands at the grid-search upper boundary, `b = 1.30`. A wider independent grid improved fit and changed 240-month gas recovery by approximately 21.7%. Gas recovery should not be externally presented until refitted with boundary diagnostics and sensitivity.
4. Observed percentiles after month 33 are affected by sample attrition. The dashboard correctly stops observed comparisons at month 33, but underlying late-time statistics should remain clearly flagged.
5. Six duplicate candidate rows collapse from 860 rows to 854 unique APIs. This did not affect the selected cohort, but uniqueness resolution should be explicit.
6. Reproducibility needs a concise run order, input manifest, file hashes, software versions, and explicit exclusion reason codes.

## Independently Verified

- First-positive normalization removed 109 pre-positive rows.
- No duplicate well-months or calendar gaps were found in the selected cohort.
- Ninety-five zero-production months after first positive production were retained.
- Monthly percentiles reproduce using inclusive linear percentiles.
- Oil fit reproduces at approximately `qi = 28,972.63 bbl/month`, `Di = 23.5%/month`, and `b = 0.85`.
- Terminal transition occurs at approximately month-on-production 144.
- Dashboard headline values reconcile with the processed data.
- Workbook scan reports zero formula errors.
- Rendered workbook sheets are legible and internally consistent.

## Minimum External-Release Package

1. Resolve or prominently disclose completion-archive selection bias.
2. Correct the EUR / 20-year cumulative label.
3. Reconcile vintage and FracFocus methodology statements.
4. Suppress or refit the current gas recovery forecast.
5. Add reproducibility instructions, source-file inventory, hashes, and explicit exclusion codes.
6. Run the judge again after corrections.

## Remediation Status - June 21, 2026

Completed:

- Replaced `Fitted Oil EUR` with `Modeled Oil to Rate Cutoff`.
- Extended the oil calculation to 360 months; oil falls below the 250 bbl/month rate cutoff at month 242.
- Revised modeled oil through the rate cutoff to approximately 433,696 bbl.
- Suppressed the gas forecast from external use because the gas fit reached the search-grid boundary.
- Reconciled the executed vintage to 2022-2023.
- Marked FracFocus as a future enhancement rather than an executed join.
- Added availability-constrained convenience-cohort language to the dashboard and methodology.
- Added explicit exclusion codes to the selection log.
- Added a reproducibility guide, critical-input SHA-256 manifest, archive inventory, runtime version, and run order.
- Rebuilt and visually verified the workbook with zero formula errors.

Remaining blocker:

- Acquire the remaining completion archives beyond the current January-February subset, rerun the cohort, and repeat independent judging before describing the sample as representative.
