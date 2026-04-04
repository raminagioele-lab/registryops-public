# RegistryOps V1 Surface Types

This document defines the closed set of authorized `surface_type` values for RegistryOps V1.

This document is subordinate to **RegistryOps V1 Canonical Specification**.

In case of divergence, **RegistryOps V1 Canonical Specification** prevails.

## Scope

RegistryOps V1 authorizes only a minimal closed vocabulary of surface types.

The purpose of this vocabulary is to constrain observation to explicitly authorized public infrastructural surfaces and to prevent taxonomic drift across observers and implementations.

No `surface_type` outside this document is allowed in RegistryOps V1.

## Authorized `surface_type` Values

RegistryOps V1 authorizes only the following values:

- `oci_manifest`
- `npm_package_metadata`
- `pypi_release_metadata`
- `github_release_asset`
- `crl_publication`
- `ct_log_entry`
- `ietf_internet_draft`

No other `surface_type` value is allowed in RegistryOps V1.

## Normative Semantics

### `oci_manifest`

Observation of the public correspondence between an OCI image reference and its manifest digest.

This surface captures the publicly observable state linking an OCI image reference to a manifest-level identifier.

### `npm_package_metadata`

Observation of the public metadata of an npm package version.

This surface captures publicly accessible release metadata relevant to an npm package version as exposed on the public npm surface.

### `pypi_release_metadata`

Observation of the public metadata of a PyPI release and its distribution artifacts.

This surface captures publicly accessible release metadata associated with a Python package release on the public PyPI surface.

### `github_release_asset`

Observation of the public metadata of assets attached to a GitHub release.

This surface captures publicly accessible metadata associated with release assets exposed through a public GitHub release surface.

### `crl_publication`

Observation of the public publication state and evolution of a Certificate Revocation List.

This surface captures publicly observable publication and change states of a CRL as exposed through a public certificate infrastructure surface.

### `ct_log_entry`

Observation of the appearance of a certificate in a public Certificate Transparency log.

This surface captures the public logging presence of a certificate entry in a Certificate Transparency system.

### `ietf_internet_draft`

Observation of successive publicly accessible versions of an IETF Internet Draft.

This surface captures the publicly observable versioned publication state of an Internet Draft within the IETF document surface.

## Closed Vocabulary Rule

The `surface_type` vocabulary of RegistryOps V1 is closed.

The following categories of values are not allowed in V1:

- legacy surface names
- generic infrastructure classes not explicitly authorized in the canonical specification
- observer-specific surface names
- compatibility aliases
- local implementation-defined surface extensions

Any extension of the `surface_type` vocabulary requires an explicit revision of the canonical specification and therefore belongs to a future version, not to V1.

## Compliance Rule

An implementation is compliant with RegistryOps V1 only if it emits events using exclusively the seven authorized `surface_type` values defined in this document and in the canonical specification.