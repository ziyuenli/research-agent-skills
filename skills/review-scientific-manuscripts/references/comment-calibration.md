# Comment Calibration

## Claim strength

| Evidence | Calibrated wording |
|---|---|
| Required definition absent | “The manuscript does not define…” |
| Brief rationale present but integration unclear | “Individual choices receive limited justification, but their combined role is insufficiently explained.” |
| Result differs across text and figure | “The text and Figure X appear inconsistent…” |
| Calculation reconstructed from context | “If the authors calculate X as inferred here, then…” |
| Evidence unavailable | “This cannot be verified from the submitted material.” |

## Common checks

- A stochastic rerun differing from the original can indicate instability, a changed seed/configuration, label alignment, or reporting error; do not choose one cause without evidence.
- A conventional criterion such as BIC must be checked against the manuscript's sign convention before calling its inequality reversed.
- A weighting rule based on time-series standard deviation requires the exact estimator, preprocessing, missing-data policy, detrending, and robustness treatment.
- Irregular temporal sampling requires checking whether covariance is indexed by observation order or actual time separation.
- A figure/network description must be checked against acquisition geometry and caption, not inferred from colors alone.

## Actionability

Request the smallest revision that resolves the defect:

- define an estimator;
- provide a rationale;
- report sensitivity analysis;
- reconcile text and figure;
- expose stochastic settings;
- add missing uncertainty;
- moderate an unsupported conclusion.

Do not demand a new experiment when clarification or a bounded analysis is sufficient.

