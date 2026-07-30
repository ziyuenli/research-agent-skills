# GAMMA Adapter

Read this reference when a workflow uses GAMMA parameter files, raw rasters, Python bindings, or command-line programs. Inspect the locally installed version and wrappers because signatures and status behavior can differ.

## Parameter files

GAMMA parameter files commonly use `key: value units-or-description`. Query by key, not fixed line number:

```bash
python scripts/query_gamma_par.py scene.par width nlines
python scripts/query_gamma_par.py dem.par corner_lat corner_north --first-present --value-only
```

Treat parameter names as format-specific. Common metadata may include width, line count, image format, range/azimuth spacing, corner coordinates, and projection details. Do not substitute one coordinate field for another without checking the coordinate system.

## Raw raster contract

Before opening a raster, determine:

- samples per line and number of lines;
- scalar or complex representation;
- bytes per component;
- byte order;
- header or offset, if any.

For headerless complex rasters, the expected size is:

`width × nlines × 2 components × bytes per component`

Common GAMMA complex representations include big-endian signed 16-bit components (`SCOMPLEX`, 4 bytes per complex sample) and big-endian 32-bit floating components (`FCOMPLEX`, 8 bytes per complex sample). Confirm against the actual metadata and local tools rather than inferring solely from the filename.

Read and write in line blocks for large scenes. Preserve byte order in outputs. After writing, verify exact byte size and reopen representative blocks using the declared dtype.

## Coregistration and offsets

- Record reference and secondary acquisitions, looks, geometry products, and command arguments.
- Retain and parse coregistration quality artifacts rather than relying only on command success.
- Inspect local Python bindings or wrapper source to learn whether failure is reported by exception, integer status, returned object, or output-file absence.
- For an `auto` initial-offset mode, try the noninteractive estimator first; preserve its status and diagnostics; enter manual selection only on a verified failure condition.
- State display requirements before launching a manual tool and provide a noninteractive failure path for headless systems.

## Acquisition discovery

Extract dates with an anchored naming rule, sort them deterministically, and detect:

- duplicate rasters for one date;
- parameter files without rasters;
- rasters without parameter files;
- reference dates absent from the inventory;
- derived files accidentally included as source acquisitions.

Generate inventory files atomically and show the proposed contents before replacing an existing operator-maintained list.

## Licensed interface boundary

Do not copy proprietary GAMMA source or undocumented implementation details into a portable skill. It is acceptable to inspect the user's licensed local installation to call its public interface correctly. Keep local installation paths, command availability, and version differences outside reusable repository content.
