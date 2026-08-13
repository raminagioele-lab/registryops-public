# RegistryOps Phase 2 Activation Dossier: crates.io Package Index Metadata

## Status

This document defines the active phase 2 surface for crates.io package index
metadata.

The canonical `surface_type` is:

```text
crates_io_package_index_metadata
```

This value is admissible in the canonical RegistryOps event model from the
governed crates.io phase 2 activation onward.

Pre-activation candidate observations produced under this dossier remain local
operational evidence only and are not retroactively promoted into
`registry/data/events.jsonl`.

## Purpose

The purpose of this surface is to observe the public temporal state of crate
version entries in the crates.io package index.

crates.io is a major software supply-chain distribution surface for the Rust
ecosystem. Its index exposes stable crate/version metadata, checksums,
dependencies, feature declarations, and the `yanked` flag.

The `yanked` flag is strategically important because it can change after a
version has been published. RegistryOps activates this surface after candidate
cycles demonstrated stable source reconstruction, deterministic fingerprints,
and low operational risk.

## Primary References

The activation dossier is based on the following primary public references:

- Cargo registry index:
  `https://doc.rust-lang.org/cargo/reference/registry-index.html`
- Cargo registries:
  `https://doc.rust-lang.org/cargo/reference/registries.html`

## Canonical Boundary

The canonical surface is limited to public sparse index entries served from:

```text
https://index.crates.io/
```

It includes:

- crate name
- exact crate version
- checksum `cksum`
- dependency metadata from the index entry
- features and features2 metadata
- `yanked`
- `links`
- `rust_version`
- index schema version field `v`
- SHA-256 of the exact target index line observed

It excludes:

- crate archive body hashing
- crates.io API metadata
- GitHub repository metadata
- downloads, popularity, ownership, teams, users, or publisher identity
- private registries
- authenticated endpoints
- local Cargo caches

These exclusions keep the surface small, deterministic, and low-risk from a
personal-data perspective.

## Canonical Asset Reference

The canonical `asset_ref` grammar is:

```text
<crate_name>@<version>
```

Examples:

```text
serde@1.0.197
tokio@1.36.0
clap@4.5.4
```

Field rules:

- `crate_name` must use lowercase ASCII letters, digits, `_`, or `-`.
- `version` is the exact version string as published in the index.
- field separators are literal `@` characters.
- fields must not contain `/`, whitespace, query syntax, fragment syntax, or
  empty values.

The recommended validation pattern is:

```text
^[a-z0-9_-]+@[A-Za-z0-9][A-Za-z0-9.+_-]*$
```

## Canonical Source Reference

The canonical `source_ref` grammar is:

```text
https://index.crates.io/<cargo-index-path>
```

where `<cargo-index-path>` is the sparse index path derived from the crate name
according to Cargo registry index rules:

- one-character crate: `1/<crate>`
- two-character crate: `2/<crate>`
- three-character crate: `3/<first-character>/<crate>`
- four or more characters: `<first-two>/<second-two>/<crate>`

Examples:

```text
https://index.crates.io/se/rd/serde
https://index.crates.io/to/ki/tokio
https://index.crates.io/cl/ap/clap
```

The only allowed host for the canonical surface is:

```text
index.crates.io
```

Equivalent Git index paths are not accepted by the canonical surface. This
keeps the public source path simple and avoids two sources representing the
same observed object.

## Observed-State Profile

The observed-state profile is the governed public state committed through
`observable_fingerprint`.

It contains:

- `surface_type`
- `asset_ref`
- `source_ref`
- `index_resource`
- `version_entry`

The `index_resource` object contains:

- `url`
- `http_status`

The `version_entry` object contains:

- `present`
- `line_number`
- `line_sha256`
- `name`
- `vers`
- `cksum`
- `deps`
- `features`
- `features2`
- `yanked`
- `links`
- `rust_version`
- `v`

RegistryOps does not publish the full observed-state profile in canonical
events. Operational receipts may store it locally under `ops_state/phase2/` for
diagnostics and audit support.

## Normalization Rules

The canonical observer must normalize the observed-state profile as follows:

- JSON is serialized with sorted keys, compact separators, UTF-8 encoding, and
  no ASCII escaping.
- the index file is decoded as UTF-8 text.
- blank lines in the index file are ignored.
- each non-blank line must be valid JSON.
- `line_sha256` is the SHA-256 of the exact raw UTF-8 target line without its
  trailing newline.
- absent optional fields are represented as `null`.
- absent maps are represented as empty JSON objects.
- absent dependency lists are represented as empty JSON arrays.
- response date, server, cache, CDN, and transfer headers are excluded from the
  profile.

## Observable Fingerprint

The canonical `observable_fingerprint` is:

```text
sha256(canonical_json_bytes(observed_state))
```

The fingerprint commits to the public crates.io index entry observed for the
target crate version.

It does not claim to hash the `.crate` archive body or any repository content.

## Canonical Outcome Classification

The canonical observer admits an observation event only when the sparse index
resource is reachable and contains the target crate version.

If the observed-state fingerprint differs from the latest canonical observation
for the same `asset_ref`, the event is classified as `state_changed`.

If the observed-state fingerprint is unchanged and the minimum cadence has
elapsed, the event is classified as `reobserved`.

If no prior canonical observation exists, the event is classified as
`first_seen`.

If the resource is absent, unreachable, rate-limited, malformed, or does not
contain the target version, the canonical observer rejects the observation for
that cycle rather than inventing a successful public state.

## Cadence Rule

The canonical cadence remains conservative:

- run observation through the official RegistryOps cadence
- avoid parallel bursts against `index.crates.io`
- use at most one public HTTP request per target per cycle
- use at most one request per second to `index.crates.io`

Unchanged observations become canonical `reobserved` events only when the
general RegistryOps minimum reobservation interval is satisfied.

## Non-Personal-Data Review

This surface is acceptable from a non-personal-data perspective only under the
following constraint:

- public canonical events, if this surface is later activated, must publish
  only `asset_ref`, `surface_type`, `event_type`, `observed_at`, `source_ref`,
  and `observable_fingerprint`.

The canonical surface must not publish owners, maintainers, user handles, teams,
download statistics, or crates.io account metadata.

## Public Verification Story

A third party can verify a canonical crates.io event by:

1. Reading the event from `journal/events.jsonl`.
2. Reconstructing the sparse index URL from `asset_ref`.
3. Fetching the public index resource from `index.crates.io`.
4. Locating the target crate version line.
5. Building the observed-state profile according to this dossier.
6. Recomputing `observable_fingerprint`.
7. Checking that the fingerprint matches the event line.
8. Verifying that the event line is included in the snapshot journal.
9. Recomputing the snapshot Merkle root from `journal/events.jsonl`.
10. Checking the root and OTS proof status according to the public RegistryOps
    proof contract.

This proves what crates.io index state RegistryOps committed at observation
time. It does not prove that crates.io never served a different state to
another observer.

## Canonical Watchlist Seed

The initial canonical watchlist seed uses stable, widely used crate versions:

```text
serde@1.0.197
tokio@1.36.0
clap@4.5.4
```

These targets may be extended only through governed watchlist changes.

## Pre-Activation Candidate Observation Mode

Before activation, the candidate observer was:

```text
registry/scripts/observe_crates_io_candidate.py
```

Its candidate watchlist is:

```text
observation/phase2_crates_io_candidates.json
```

That mode writes only local operational candidate receipts under:

```text
ops_state/phase2/
```

It must not write to:

- `registry/data/events.jsonl`
- `registry/ingestion/observation_receipts.jsonl`
- `registry/ingestion/observation_cycles.jsonl`
- `registry/taxonomy/`
- `registry/schemas/`

Pre-activation candidate observations are evidence for design validation. They
are not canonical RegistryOps events.

## Activation Checklist

This activation closes the following requirements:

- taxonomy entry for `crates_io_package_index_metadata`
- surface rules entry with the grammar defined here
- event schema compatibility for the new surface
- canonical observer integration
- deterministic observed-state profile tests
- source URL reconstruction tests
- yanked-state behavior tests
- pre-activation stability over multiple candidate observation cycles
- operational monitor coverage
- public governance file inclusion policy
