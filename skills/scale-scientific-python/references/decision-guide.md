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
- PSS and private dirty memory per worker, not only RSS;
- maximum in-flight input and output bytes;
- serialization volume;
- expected storage bandwidth per worker;
- native thread count multiplied by process count;
- NUMA nodes crossed by each process and whether first-touch placement is controlled;
- local-disk versus network-filesystem traffic for the actual access pattern.

If throughput plateaus as workers increase, test for storage saturation, memory bandwidth, lock contention, queue backpressure, task imbalance, native threading, or an effectively serial setup/merge stage.

Measure a native executable separately from its Python wrapper. Inspect the process's effective environment and linked runtime; shell configuration does not prove what an already-running process inherited.

On Linux, interpret `MemAvailable`, page-cache size, PSS, shared clean/dirty,
and private dirty pages together. Low `MemFree` alone is not evidence of
pressure, and summed worker RSS can count the same shared pages repeatedly.
Watch copy-on-write growth after `fork`, especially when inherited solver or
preconditioner objects mutate internal buffers.

On a multi-socket host, benchmark one NUMA node before spanning sockets. Pin
workers and apply first touch or local allocation consistently; compare this
with interleaving only when the working set cannot fit locally. Count physical
cores separately from simultaneous-multithreading threads.

## Chunk and memmap contracts

Record dtype, full shape, logical axes, byte order, chunk boundaries, completion state, and index mapping. A worker should receive a small descriptor such as a path plus slice, reopen the mapping locally, and write only its assigned output slice.

Test:

1. empty and one-element chunks;
2. final partial chunks;
3. boundaries that cross masks or graph partitions;
4. non-contiguous requested indices;
5. interrupted output and rerun behavior;
6. full-versus-chunked numerical equivalence.
7. cross-chunk constraints and global offsets for graph or inverse problems.

## Sparse systems

Separate reusable state from per-solve state:

- topology depends on node/edge connectivity;
- weights and diagonal depend on the weighted operator;
- the preconditioner depends on the operator and its configuration;
- the right-hand side depends on observations;
- work buffers depend on shape and dtype.

Reuse topology or preconditioners only while their dependencies remain identical. Benchmark operator construction, preconditioner setup, each iteration, total solve time, iteration count, and residual quality.

A matrix-free operator is attractive when explicit sparse assembly is a major memory or setup cost and the solver needs only matrix-vector products. An explicit matrix remains useful when a preconditioner or factorization requires it and amortizes its construction across many solves.

A reusable solver context can cache topology, maps, capacities, costs, and
allocation without providing a warm start. Check the library's repeated-run
semantics. For a controlled comparison:

1. feed every variant the same cached graph and observation rows;
2. preserve graph insertion order, solver template types, cost/capacity types,
   tolerances, and method options;
3. compare setup, per-call initialization, solve, and result extraction;
4. compare status, objective, flow or solution values, and downstream
   residuals;
5. then vary one solver type, dtype, or reuse policy at a time.

Persistent contexts trade repeated setup for resident per-worker state.
Measure both throughput and private memory at the intended worker count.

## Benchmark contract

- Use the same input, tolerance, thread settings, cache state, and output checks.
- Include a correctness baseline before performance comparisons.
- Record wall time, CPU time where useful, peak RSS and PSS, private dirty
  memory, bytes read/written, workers, native threads, affinity, NUMA policy,
  iterations, and hardware.
- Run enough repetitions to reveal variance.
- Explain whether the result is a microbenchmark, representative subset, or full workload.
- Do not infer the cause of a whole-run regression from a commit containing
  multiple algorithm, dtype, storage, or execution changes. Replay the
  suspected stage from fixed cached inputs.
