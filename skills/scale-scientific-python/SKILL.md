---
name: scale-scientific-python
description: Diagnose and optimize large scientific Python workloads using NumPy, SciPy, memmap, multiprocessing, sparse graphs, and iterative solvers. Use for slow or memory-heavy array pipelines, larger-than-RAM processing, chunked-versus-full computation, serial-versus-parallel scaling, costly indexing or I/O, tens of millions of graph edges, matrix-free operators, preconditioner reuse, or decisions about vectorization, compiled kernels, multiprocessing, and storage layout.
---

# Scale Scientific Python

Optimize from measured evidence while preserving scientific results. Do not claim a speedup until a representative benchmark demonstrates it.

## Workflow

1. Define the invariant output, numerical tolerance, ordering, dtype, shape, and reproducibility requirements.
2. Measure the current path on representative data. Separate compute time, storage I/O, allocation, serialization, synchronization, and result collection.
   Inspect the effective native thread count, CPU affinity, NUMA placement, mount type, and storage location when the workload runs on a server.
3. Estimate peak resident memory, temporary allocations, bytes read and written, and process multiplication before selecting an approach.
4. Rank viable approaches and recommend one using the current evidence. Read [decision-guide.md](references/decision-guide.md) when comparing memory layouts, concurrency models, or sparse-solver strategies.
5. For an initial algorithm draft, implement one minimal end-to-end path. Do not add alternative solvers, preconditioners, backends, flags, or abstraction layers merely because they were discussed.
6. Validate the central assumption and scientific output, then iterate only when evidence or an explicit comparison request justifies another approach.
7. Implement one material change at a time and retain a correct baseline until equivalence is established.
8. Validate correctness first, then benchmark warm and cold behavior where caching matters.

## Preserve data semantics

- Treat array index order, graph node and edge mappings, masks, slices, sentinels, and boundary behavior as explicit invariants.
- Compare chunked output with the full-array implementation on synthetic edge cases and representative data.
- Compare serial and parallel output independently of completion order.
- Use explicit tolerances appropriate to dtype and conditioning; report maximum error and failing counts, not only a Boolean result.
- Confirm that changed preconditioners alter convergence behavior rather than the converged mathematical solution, subject to tolerance and solver termination.

## Design for memory and I/O

- Avoid hidden full-size copies from fancy indexing, dtype promotion, reshaping, concatenation, or process serialization.
- Prefer sequential block access when storage locality dominates; use gathered indexing only after measuring it.
- Use memmap for shared, read-mostly, larger-than-RAM arrays when its access pattern is controlled. Flush completed outputs and store enough metadata to reopen them safely.
- Write each output region from exactly one process unless synchronization is intentional.
- Bound queues and in-flight tasks. A queue is not a substitute for a memory budget.
- Clean up incomplete temporary products or mark them invalid so reruns cannot consume partial data.

## Parallelize deliberately

- Determine whether work is CPU-bound, I/O-bound, memory-bandwidth-bound, or blocked by native-library threading.
- Distinguish Python workers from native OpenMP, BLAS, solver, or compiled-extension threads. A large thread count is not evidence of a Python GIL bottleneck.
- Prefer processes for CPU-bound Python work, but account for startup, pickling, result transfer, and duplicated state.
- Pass compact descriptors to workers; reopen memmaps or shared resources inside the worker when practical.
- Prevent oversubscription from BLAS, OpenMP, NumPy/SciPy, or nested process pools.
- Test `1, 2, 4, ...` workers under fixed native-thread settings. Select the knee of measured throughput rather than the logical CPU count.
- Choose task sizes large enough to amortize dispatch and small enough to balance skew and memory.
- Use explicit worker error propagation, termination, joins, and output-completeness checks.

## Optimize sparse graphs and solvers

- Avoid materializing COO/CSR matrices when a matrix-free operator provides the required operations more cheaply.
- Cache graph topology, weights, diagonal terms, preconditioners, and work buffers only when their dependencies are unchanged.
- Do not cache an object across iterations merely because dimensions match; state the dependency invariant.
- Benchmark setup and solve phases separately. A cheaper setup can lose overall if convergence worsens.
- Treat `np.add.at`, sparse construction, and compiled kernels as candidates to measure, not automatic improvements.
- Separate static topology from per-observation values. Reuse node mappings, edge endpoints, CSR structure, and graph partitions only when their dependency invariants hold.

## Partition global problems carefully

- Do not assume that blocking a raster preserves a global graph solution.
- For local filters and gradients, use halos sized to the operator support.
- For phase unwrapping, MCF, connected components, or Laplacian systems, identify cross-block constraints before partitioning.
- Validate any overlap-and-reconciliation method against a full small case. Report boundary discontinuities, component splits, global integer offsets, and loss of path consistency.
- Use local scratch for metadata-heavy or line-oriented intermediate I/O only after comparing it with the mounted storage on the same access pattern.

## Report

Give the bottleneck diagnosis, selected intervention, correctness evidence, and before/after timing, peak memory, I/O volume, worker count, and dataset scale. If a representative run was not possible, label estimates as estimates.
