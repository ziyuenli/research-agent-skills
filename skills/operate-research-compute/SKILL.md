---
name: operate-research-compute
description: Diagnose and safely operate research workstations, Linux servers, NAS/NFS storage, multi-user environments, VPN-dependent networking, SSH tunnels, VNC sessions, OpenMP runtimes, and scientific software installations. Use for slow remote processing, excessive native threads, NUMA or storage contention, per-user environment or permission problems, broken connectivity after VPN changes, stale VNC displays, SSH port forwarding, or system configuration changes that must preserve the active connection.
---

# Operate Research Compute

Preserve access first. Diagnose from observable state before changing network, login, storage, permission, or runtime configuration.

## Establish the control path

Record:

- local and remote host roles;
- how the current session depends on VPN, SSH, VNC, or a mounted filesystem;
- whether losing that path would stop the work;
- user privileges and whether configuration is global or per-user;
- the exact process, command, mount, port, and affected users.

Never disconnect or reconfigure the only active control path during diagnosis. If a proposed change may drop the session, prepare an independent recovery path or ask the user to execute it locally.

Read [diagnostic-playbooks.md](references/diagnostic-playbooks.md) for focused checks.

## Diagnose read-only

1. Reproduce the symptom and timestamp it.
2. Separate network reachability, name resolution, routing, proxy/VPN state, application configuration, and remote service health.
3. For performance, separate CPU work, runnable threads, I/O wait, memory pressure, NUMA placement, and network storage.
4. Compare a failing user or host with a working one.
5. Inspect the effective process environment, not merely configuration files.
6. Check login-shell, interactive-shell, Conda, scheduler, and service-manager inheritance independently.

## Change the narrowest layer

- Prefer a per-command or per-application setting while testing.
- Apply global limits only when the policy is intended for every user.
- Preserve existing sudoers, shell, mount, and service configuration.
- Validate syntax before reloading a service.
- Keep a rollback command or backup for material configuration changes.
- Do not expose VNC directly when an SSH tunnel provides the required access.

## Verify

After a change:

- open a fresh login session rather than trusting the inherited environment;
- inspect the target process's actual thread count and environment;
- rerun the same workload and compare elapsed time, CPU time, I/O wait, and output;
- verify unaffected users and services;
- confirm that VPN, SSH, VNC, and mounts still work;
- document scope: one command, one user, one software stack, or system-wide.

