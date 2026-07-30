# Diagnostic Playbooks

## Native-thread explosion

Check:

- process and thread count;
- linked OpenMP runtime;
- effective `OMP_*`, `MKL_*`, `OPENBLAS_*`, and related variables;
- sockets, physical cores, SMT threads, NUMA nodes, and CPU affinity;
- whether the program is compute-bound or stalled on storage.

Large thread count is not proof of a GIL problem. Native scientific executables can create OpenMP threads without Python. Compare elapsed time, CPU time, context switches, and I/O wait before concluding that oversubscription is causal.

Test a per-command thread limit first. A global `/etc/profile.d/` setting affects login shells that source it, not necessarily existing sessions, services, schedulers, or Conda activation scripts. Verify with a fresh login and the running process.

## NAS/NFS performance

Inspect mount type and options, network link, server load, file size distribution, metadata rate, sequential throughput, and local scratch availability. A 10 Gb link does not guarantee low latency or good small-file performance.

Benchmark the same read/write pattern on local scratch and the mount. Keep source data on shared storage when required, but stage temporary line-oriented or metadata-heavy processing locally when measurements justify it.

NFS ownership and permissions may be governed by server-side UID/GID mapping, root squashing, ACLs, or the NAS management layer. A client-side `chown` failure is not solved by repeatedly using sudo.

## VPN-dependent connectivity

Capture routes, DNS, proxy state, and application split-tunneling rules while the VPN is working and failing. Do not disconnect the VPN when it carries the active Codex or SSH session. Prefer a reversible setting change that preserves the tunnel and verify from a second terminal.

## VNC through SSH

Treat display `:N` and TCP port `5900+N` distinctly. Confirm that the VNC process is live rather than stale and whether it listens only on loopback.

For loopback-only VNC, keep an SSH local forward active:

```bash
ssh -fN \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -L LOCAL_PORT:127.0.0.1:REMOTE_PORT \
  user@host
```

Connect the viewer to the local forwarded port. Prefer an SSH config entry or supervised tunnel over exposing the VNC port externally.

## Multi-user configuration

Compare:

- `getent passwd USER`;
- fresh login-shell environment;
- interactive-shell environment;
- user dotfiles after Conda initialization;
- service or scheduler environment;
- UID/GID and supplementary groups;
- ACLs and server-side share permissions.

State explicitly whether a change affects one process, one user, all login users, or the whole system.

