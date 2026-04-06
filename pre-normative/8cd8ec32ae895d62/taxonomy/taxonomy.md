# RegistryOps Taxonomy Index

This document provides the canonical taxonomy index for RegistryOps.

It summarizes the closed vocabularies used by RegistryOps and points to the dedicated taxonomy documents for event types and surface types.

This document is subordinate to the RegistryOps Canonical Specification.

In case of divergence, the RegistryOps Canonical Specification prevails.

## Scope

RegistryOps uses a closed taxonomy.

The taxonomy is intentionally minimal.

Its purpose is to preserve semantic consistency across observers, schemas, ingestion logic, validation rules, and public publication outputs.

No taxonomy outside the canonical specification and its subordinate taxonomy documents is allowed in RegistryOps.

## Taxonomy Components

RegistryOps uses two closed vocabularies:

- `event_type`
- `surface_type`

These vocabularies are defined in the following documents:

- `registry/taxonomy/event_types.md`
- `registry/taxonomy/surfaces.md`

## Authorized `event_type` Values

RegistryOps authorizes only the following `event_type` values:

- `first_seen`
- `state_changed`
- `withdrawn`
- `revoked`
- `replaced`
- `expired`
- `unreachable`

No other `event_type` value is allowed in the canonical taxonomy.

## Authorized `surface_type` Values

RegistryOps authorizes only the following `surface_type` values:

- `oci_manifest`
- `npm_package_metadata`
- `pypi_release_metadata`
- `github_release_asset`
- `crl_publication`
- `ct_log_entry`
- `ietf_internet_draft`

No other `surface_type` value is allowed in the canonical taxonomy.

## Closed Taxonomy Rule

RegistryOps taxonomy is closed.

This means that:

- no legacy taxonomy remains valid in the canonical taxonomy
- no implementation-defined taxonomy extension is allowed in the canonical taxonomy
- no observer-specific taxonomy is allowed in the canonical taxonomy
- no compatibility alias is allowed in the canonical taxonomy

Any taxonomy extension requires an explicit revision of the canonical specification and therefore belongs to a future governed revision, not to the current canonical taxonomy.

## Compliance Rule

An implementation is compliant with RegistryOps only if it uses exclusively the authorized `event_type` and `surface_type` vocabularies defined in the canonical specification and in the subordinate taxonomy documents.