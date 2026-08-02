# Project Charter: Classical DCA vs Machine Learning Forecasting

## Working Title

Classical DCA vs Machine Learning Forecasting on a Public Permian Production Cohort

## Project Purpose

This project is a learning and portfolio project. The goal is to compare classical decline curve analysis (DCA) with simple machine learning forecasting methods using public Permian Basin production data.

The project should demonstrate that I can:

- use Python for a real technical data workflow;
- translate reservoir engineering judgment into reproducible analysis;
- compare machine learning against domain-informed baselines;
- evaluate forecast accuracy, bias, and uncertainty honestly;
- communicate model limitations clearly.

## Core Research Question

Can simple machine learning models improve short-horizon oil production forecasts compared with classical decline curve analysis and simple time-series baselines on a public Permian production cohort?

## Secondary Questions

- When does a simple baseline, such as last observed rate, outperform more complex models?
- How do DCA and ML differ in interpretability and decision usefulness?
- How sensitive are conclusions to the train/test split and forecast horizon?
- What model limitations should be communicated before using forecasts in decision-making?

## Dataset Starting Point

The starting dataset comes from the prior SEM UT Dallas Permian type-curve project.

Initial processed file:

`data/processed/martin_selected_30_monthly_production_normalized.csv`

Known facts from the prior project:

- Geography: Martin County, Texas, Midland Basin / Permian Basin.
- Cohort: 30 selected Pioneer horizontal oil wells.
- Source: public Railroad Commission of Texas data.
- Normalized production rows: 1,220.
- Wells: 30.
- Maximum month on production: 54.
- Full cohort present through month 33.

## Data Boundary

This project will not claim to be a representative Permian population study.

The cohort is an availability-constrained convenience cohort. The prior QA review found that completion archive coverage was incomplete, so the sample should not be described as representative of all Pioneer wells or all Martin County wells.

The first release will focus on oil forecasting. Gas forecasting will be excluded unless separately remediated, because the prior gas decline fit reached a boundary and was suppressed from external use.

## Planned Methods

### 1. Data Understanding and QA

Tasks:

- inspect the production data schema;
- confirm well count, row count, and production-month coverage;
- create a data dictionary;
- identify missing values, zero-production months, and possible outliers;
- document limitations.

Deliverables:

- data dictionary;
- data QA notes;
- first exploratory plots.

### 2. Analytical DCA

Tasks:

- implement exponential decline;
- implement hyperbolic decline;
- optionally discuss harmonic decline;
- fit decline models to selected wells and/or the P50 type curve;
- forecast future monthly oil production;
- compare fitted and observed rates;
- compute cumulative oil over a defined forecast horizon.

Deliverables:

- DCA methods note;
- fitted parameters;
- DCA forecast plots;
- DCA error metrics.

### 3. Python / ML Forecasting

Tasks:

- create lag features;
- create rolling average features;
- define a time-based train/test split;
- train simple ML models such as random forest and gradient boosting;
- include a naive baseline such as last observed rate;
- compare model performance.

Deliverables:

- ML workflow script or notebook;
- feature list;
- model comparison table;
- forecast-vs-actual plots.

### 4. Model Comparison

Tasks:

- compare DCA, ML, and naive baselines;
- evaluate MAE, RMSE, sMAPE, and bias;
- inspect errors by month on production;
- identify where each method performs well or poorly;
- discuss interpretability and uncertainty.

Deliverables:

- model comparison report;
- final figures;
- summary of lessons learned.

### 5. GitHub Packaging

Tasks:

- create a clean repository structure;
- write a clear README;
- include reproducibility instructions;
- include data limitations;
- organize code, notebooks, reports, and figures;
- decide whether to include processed data or provide instructions to reproduce it.

Deliverables:

- GitHub-ready repo;
- README;
- final report;
- requirements file.

## Initial Project Structure

```text
ai-ml-dca-permian/
  README.md
  PROJECT_CHARTER.md
  data/
    processed/
  notebooks/
  src/
    dca_ml/
  reports/
    figures/
    data_dictionary.md
    data_limitations.md
    final_report.md
  requirements.txt
  .gitignore
```

## Success Criteria

The project is successful if I can explain:

- where the data came from;
- what each column means;
- why the cohort is limited;
- how DCA works conceptually and mathematically;
- how the ML features were created;
- why the train/test split avoids future leakage;
- which model performed best and why;
- whether ML improved the forecast;
- what limitations would matter before using the forecast in real decisions.

## Red-Team Questions

Before publishing, test the project against these questions:

- Am I accidentally claiming the cohort is representative?
- Did I use future data in training or features?
- Did I compare ML against weak baselines only?
- Can I explain every model and metric without hiding behind jargon?
- Are the limitations clear enough that a skeptical reviewer would trust the work?
- Does the project show learning and judgment, not just code execution?

## First Decision Gates

Before writing code, confirm:

1. Use the existing Martin County 30-well cohort as the first dataset.
2. Focus the first release on oil production only.
3. Treat this as a model-comparison and learning project, not a reserves report.
4. Build the project step by step, with explanations and notes after each stage.

## Current Status

Planning phase. No final project execution has started in this fresh-start folder.
