# RegistryOps Migration Status

RegistryOps distinguishes between:

- the canonical phase 1 publication line
- pre-normative historical publications that had a real public existence

## Canonical Line

The canonical phase 1 line starts at:

`snapshots/phase1-000001/`

From that point onward, `current/` must reference only canonical phase 1
snapshots.

## Pre-Normative History

Public artifacts that existed before the closure of the phase 1 normative
framework may be preserved under:

`pre-normative/<publication_id>/`

These artifacts remain historically valuable but are not presumed to satisfy
the stabilized phase 1 public contract.

## Internal Pre-Normative Artifacts

Artifacts that never had a public existence and do not provide explicit
migration, audit, or traceability value are outside the official public archive
of RegistryOps phase 1.
