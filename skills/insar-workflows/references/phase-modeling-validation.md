# Phase Modeling and Validation

## Define the phase contract

State:

- acquisition index set and interferometric-pair set;
- spatial support: pixel/node, edge, or raster;
- wrapped interval and wrapping operator;
- reference acquisition or gauge constraint;
- whether a symbol denotes a random field, realization, observation, or estimate;
- graph orientation and closure sign convention.

Use exact equality only for an exact model relation. Use `:=` for definitions and congruence modulo \(2\pi\) when the equality holds only up to integer cycles.

For a closure triplet \(i<j<k\), define the oriented closure operator once and apply it consistently to node- or edge-supported pairwise phase. Check whether fractional components cancel because all pairs derive from one common phase history. Do not assume this cancellation for independently estimated interferograms.

Distinguish:

- node-balance conservation in a flow model;
- cycle closure;
- a curl-free potential flow;
- phase wrapping consistency.

They are not interchangeable constraints.

## Design simulations from the claim

1. Define the scientific feature the method must recover: spatial footprint, deformation history, discontinuity, decorrelation, or cycle error.
2. Generate the latent physical or statistical field first.
3. Apply SAR geometry and phase conversion explicitly.
4. Add nuisance components in controlled stages.
5. Use positive and negative ambiguity errors and tune their prevalence.
6. Compare corrected phase with latent phase and corrected integer ambiguity with injected ambiguity.
7. Include a small exact case before a large stochastic case.

When placing a synthetic landslide on a DEM, use raw elevation, spacing, and georeferencing. Derive slope units from terrain boundaries rather than selecting from a rendered image. Keep deformation, scattering, atmospheric, topographic-residual, and decorrelation components separately available for ablation.

## Validate coherence regularization and phase linking

- Ensure every population and estimated coherence matrix is Hermitian with unit diagonal; require positive semidefiniteness where the downstream method assumes it.
- Use the same simulated looks across competing estimators.
- Exclude the unit diagonal from off-diagonal coherence-error metrics.
- Report signed magnitude bias, weak-coherence error, phase RMSE, circular bias, gross cycle-error rate, runtime, and Monte Carlo uncertainty.
- Test multiple sample-support ratios and structural models, including a deliberately misspecified model.
- Select a regularizer using held-out loss aligned with the downstream phase task when possible.

A structured shrinkage target can improve phase recovery while worsening unweighted matrix loss by suppressing harmful low-coherence pairs. Conversely, a lower magnitude NMSE can worsen phase recovery. Do not declare one estimator superior from a single matrix metric.

## Interpret Fisher information and CRLB

- Compute an oracle expected-information CRLB from the true population model when evaluating simulation efficiency.
- Call information calculated from an estimated or regularized matrix a plug-in uncertainty estimate, not a method-specific CRLB.
- Verify observed-information calculations by Monte Carlo convergence to expected information at the true parameter.
- Account for the phase reference by removing or constraining the gauge degree of freedom.
- Do not claim to beat the ordinary unbiased CRLB when estimates are biased, wrapped, multimodal, or dominated by gross errors.
- Report calibration and positive-definiteness failures of plug-in information matrices.

## Acceptance criteria

Require:

- deterministic seeds and saved configuration;
- exact formulas and sign conventions;
- representative runtime separated into estimation, regularization, phase retrieval, and uncertainty calculation;
- confidence intervals across independent trials;
- explicit limitations for Gaussian looks, homogeneous samples, closure errors, unwrapping, and target misspecification.

