# Final Summary Draft

## Question

Can simple machine learning models improve short-horizon oil production forecasts compared with classical decline-curve baselines on a public Permian production cohort?

## Current Status

The project scaffold and first ML baseline workflow are in place. The current comparison uses lagged production features and evaluates months 25-33 against a training window through month 24.

## Early Interpretation

The first run produced a useful cautionary result: the last-observed-rate baseline outperformed the initial random forest and gradient boosting models on MAE, RMSE, and sMAPE. This does not mean ML is unhelpful; it means the first ML feature set is not yet adding decision-useful signal beyond a simple time-series baseline for this short-horizon test window.

That is a good empirical starting point. The next step is to add classical DCA baselines and diagnose where each model fails by month, well maturity, and production behavior.

## AI/ML Evaluation Takeaway

The project is designed to emphasize a sober evaluation habit: compare ML against strong domain baselines, check forecast bias, and describe uncertainty and limitations clearly.
