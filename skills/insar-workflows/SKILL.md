---
name: insar-workflows
description: Build, inspect, automate, and validate SAR/InSAR processing workflows with a tool-neutral core and efficient GAMMA integration. Use for SLC or RSLC complex rasters, GAMMA parameter files and commands, coregistration, initial offsets, interferograms, multilooking, void or hole handling, phase unwrapping, acquisition-date inventories, rerun-safe shell pipelines, quality-file extraction, or adapting an existing workflow toward GAMMA, ISCE, MintPy, SNAP, or another InSAR processor.
---

# InSAR Workflows

Preserve scientific meaning and source products while making the workflow reproducible, inspectable, and rerun-safe. Treat GAMMA as a supported adapter, not as the conceptual boundary.

## Start from the dataset contract

1. Inventory acquisitions and pair each raster with its parameter and ancillary files.
2. Derive dates using an explicit naming rule such as an exact `YYYYMMDD` token; report duplicates and unmatched files.
3. Read dimensions, storage type, byte order, and geometry from authoritative metadata.
4. Verify expected byte size before reading a raw raster.
5. Identify the workflow stage, reference acquisition, coordinate system, looks, and intended downstream products.
6. Preserve original data and existing user edits. Write derived products to distinct, traceable paths.

For GAMMA formats and interface conventions, read [gamma-adapter.md](references/gamma-adapter.md). Use `scripts/query_gamma_par.py` for deterministic parameter lookup instead of fragile line-number parsing.

For phase-field notation, closure, phase-unwrapping simulations, coherence-matrix regularization, phase-linking validation, and CRLB interpretation, read [phase-modeling-validation.md](references/phase-modeling-validation.md).

## Handle invalid and void samples scientifically

- Do not assume that `0+0j`, `1+0j`, zero amplitude, NaN, or another value is invalid solely from its numeric value.
- Determine validity from format documentation, parameter metadata, masks, spatial structure, acquisition consistency, processing history, and downstream artifacts.
- Keep the invalid-data mask separate from the replacement algorithm.
- For complex filling, average complex samples only when that estimator matches the scientific intent; document neighborhood, minimum support, boundary behavior, and iteration policy.
- Prevent newly filled samples from silently becoming independent evidence in later passes unless propagation is explicitly intended.
- Validate clustered holes, borders, isolated valid islands, all-invalid neighborhoods, and both supported complex storage types.

## Build rerun-safe workflows

- Make stage inputs, outputs, completion checks, and overwrite behavior explicit.
- Treat an output as reusable only after validating its associated metadata and completeness.
- Make `--rerun` or equivalent behavior targeted: remove or replace only products owned by the selected stage.
- Quote shell paths, avoid ambiguous globs, check command status, and stop on missing mandatory inputs.
- Capture invoked commands, relevant configuration, software version, reference date, and quality summaries.
- Validate shell syntax and exercise discovery logic without launching expensive processing when possible.

## Integrate processors behind adapters

Keep these concepts processor-neutral:

- acquisition and pair inventory;
- raster and metadata contract;
- stage state and provenance;
- quality metrics;
- masks and invalid-data policy;
- validation and acceptance criteria.

Isolate processor-specific commands, status handling, filenames, and parameter keys. A future ISCE, MintPy, SNAP, or other adapter should implement the same conceptual contracts without changing the core workflow.

## Validate results

- Confirm raster dimensions, dtype, byte order, and exact file size.
- Compare input and output masks and count unresolved or unexpectedly changed pixels.
- Inspect amplitude and phase behavior, not only complex equality.
- Verify coregistration or offset quality using the processor's quality artifacts and spatial diagnostics.
- Check expected product counts and one-to-one metadata pairing.
- Run a small synthetic or cropped case before full-scene processing.
- Report commands that could not be exercised because licensed software, data, or a display was unavailable.
- When validating phase estimators, report both local error and gross-error probability. Do not interpret wrapped or circular RMSE through an ordinary unbiased CRLB when cycle slips are frequent.
- Evaluate a coherence regularizer on the downstream phase objective as well as matrix error; a lower coherence-magnitude loss need not produce lower phase error.

## Modify existing pipelines conservatively

Inspect local wrappers and bindings before assuming return-value or error semantics. Reuse established project functions when they are correct. When adding automatic/manual fallback, preserve the failure evidence from the automatic path and make interactive requirements explicit.
