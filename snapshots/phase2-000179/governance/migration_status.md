# RegistryOps Migration Status

RegistryOps distinguishes between:

- the canonical phase 1 publication line
- the canonical phase 2 publication line
- pre-normative historical publications that had a real public existence

## Canonical Lines

The canonical phase 1 line starts at:

`snapshots/phase1-000001/`

The canonical phase 2 line starts at:

`snapshots/phase2-000001/`

From phase 2 activation onward, `current/` references the active phase 2
canonical line. Earlier `phase1-*` snapshots remain preserved canonical
history.

## July 2026 Contract-Hardening Boundary

The first manifest that declares
`contract_profile = registryops-contract-2026-07` begins the prospective
hardened profile. Earlier canonical snapshots remain untouched and are
registered as a disclosed legacy baseline in `immutability_ledger.json`.

Proof maturation after this boundary is published only through immutable
`attestations/<publication_id>/<revision_id>/` revisions. It must not mutate a
snapshot or `current/`.

## Pre-Normative History

Public artifacts that existed before the closure of the phase 1 normative
framework may be preserved under:

`pre-normative/<publication_id>/`

These artifacts remain historically valuable but are not presumed to satisfy
the stabilized phase 1 public contract.

## Internal Pre-Normative Artifacts

Artifacts that never had a public existence and do not provide explicit
migration, audit, or traceability value are outside the official public archive
of RegistryOps.
