# RegistryOps V1 Taxonomy Index

This document provides the canonical taxonomy index for RegistryOps V1.

It summarizes the closed vocabularies used by RegistryOps V1 and points to the dedicated taxonomy documents for event types and surface types.

This document is subordinate to **RegistryOps V1 Canonical Specification**.

In case of divergence, **RegistryOps V1 Canonical Specification** prevails.

## Scope

RegistryOps V1 uses a closed taxonomy.

The taxonomy is intentionally minimal.

Its purpose is to preserve semantic consistency across observers, schemas, ingestion logic, validation rules, and public publication outputs.

No taxonomy outside the canonical V1 specification and its subordinate taxonomy documents is allowed in RegistryOps V1.

## Taxonomy Components

RegistryOps V1 uses two closed vocabularies:

- `event_type`
- `surface_type`

These vocabularies are defined in the following documents:

- `registry/taxonomy/event_types_v1.md`
- `registry/taxonomy/surfaces_v1.md`

## Authorized `event_type` Values

RegistryOps V1 authorizes only the following `event_type` values:

- `first_seen`
- `state_changed`
- `withdrawn`
- `revoked`
- `replaced`
- `expired`
- `unreachable`

No other `event_type` value is allowed in V1.

## Authorized `surface_type` Values

RegistryOps V1 authorizes only the following `surface_type` values:

- `oci_manifest`
- `npm_package_metadata`
- `pypi_release_metadata`
- `github_release_asset`
- `crl_publication`
- `ct_log_entry`
- `ietf_internet_draft`

No other `surface_type` value is allowed in V1.

## Closed Taxonomy Rule

RegistryOps V1 taxonomy is closed.

This means that:

- no legacy taxonomy remains valid in V1
- no implementation-defined taxonomy extension is allowed in V1
- no observer-specific taxonomy is allowed in V1
- no compatibility alias is allowed in V1

Any taxonomy extension requires an explicit revision of the canonical specification and therefore belongs to a future version, not to V1.

## Compliance Rule

An implementation is compliant with RegistryOps V1 only if it uses exclusively the authorized `event_type` and `surface_type` vocabularies defined in the canonical specification and in the subordinate taxonomy documents.