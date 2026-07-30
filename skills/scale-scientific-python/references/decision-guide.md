# Scaling Decision Guide

Use this reference after measuring the baseline. Select the simplest option that addresses the measured bottleneck.

## Array execution

| Evidence | Prefer | Watch for |
|---|---|---|
| Python-loop overhead dominates | NumPy vectorization, Numba, Cython, or a compiled extension | Temporary arrays and dtype changes |
| Working set fits RAM but copies do not | Preallocation, in-place operations, buffer reuse | Aliasing and changed numerical order |
| Working set exceeds RAM | Chunking, memmap, Zarr, or Dask where orchestration is justified | Random access, cache thrashing, partial outputs |
| Storage reads dominate | Contiguous blocks, fewer passes, compact dtype, local scratch | Fancy-index gathers and many small reads |
| Memory bandwidth dominates | Fewer passes and intermediates | More workers can make performance worse |

Do not combine multiple frameworks before establishing that one cannot meet the requirement.

## Concurrency

Use threads when native code releases the GIL and shared-memory access is the main advantage. Use processes for CPU-bound Python or isolated native calls when serialization and duplicated state are affordable. Use a distributed framework only when multi-machine scheduling, resilience, or dataset abstractions justify its overhead.

For each design, calculate:

- bytes of private state per worker;
- maximum in-flight input and output bytes;
- serialization volume;
- expected storage bandwidth per worker;
- native thread count multiplied by process count.

If throughput plateaus as workers increase, test for storage saturation, memory bandwidth, lock contention, queue backpressure, task imbalance, native threading, or an effectively serial setup/merge stage.

## Chunk and memmap contracts

Record dtype, full shape, logical axes, byte order, chunk boundaries, completion state, and index mapping. A worker should receive a small descriptor such as a path plus slice, reopen the mapping locally, and write only its assigned output slice.

Test:

1. empty and one-element chunks;
2. final partial chunks;
3. boundaries that cross masks or graph partitions;
4. non-contiguous requested indices;
5. interrupted output and rerun behavior;
6. full-versus-chunked numerical equivalence.

## Sparse systems

Separate reusable state from per-solve state:

- topology depends on node/edge connectivity;
- weights and diagonal depend on the weighted operator;
- the preconditioner depends on the operator and its configuration;
- the right-hand side depends on observations;
- work buffers depend on shape and dtype.

Reuse topology or preconditioners only while their dependencies remain identical. Benchmark operator construction, preconditioner setup, each iteration, total solve time, iteration count, and residual quality.

A matrix-free operator is attractive when explicit sparse assembly is a major memory or setup cost and the solver needs only matrix-vector products. An explicit matrix remains useful when a preconditioner or factorization requires it and amortizes its construction across many solves.

## Benchmark contract

- Use the same input, tolerance, thread settings, cache state, and output checks.
- Include a correctness baseline before performance comparisons.
- Record wall time, CPU time where useful, peak RSS, bytes read/written, workers, iterations, and hardware.
- Run enough repetitions to reveal variance.
- Explain whether the result is a microbenchmark, representative subset, or full workload.
