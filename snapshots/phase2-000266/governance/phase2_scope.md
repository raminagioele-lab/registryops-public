# RegistryOps Phase 2 Scope

RegistryOps phase 2 activates the phase 1 normative core plus two additional
software supply-chain surfaces:

- `oci_manifest`
- `npm_package_metadata`
- `pypi_release_metadata`
- `ietf_internet_draft`
- `maven_central_artifact_metadata`
- `crates_io_package_index_metadata`

These six surfaces are the active `surface_type` values admissible in the
phase 2 canonical event model.

No additional surface may be activated during the July 2026 contract-hardening
transition. Observation of these six surfaces continues without interruption.
Expansion may resume only after the hardened contract gate remains green in
official operation.

## Phase 2 Activation Rule

Phase 2 begins at the first canonical snapshot whose publication identifier
matches:

```text
phase2-000001
```

Snapshots whose identifiers match `phase1-*` remain valid canonical history for
the earlier phase 1 line. They are not rewritten or reinterpreted.

From `phase2-000001` onward, `current/` references the active phase 2 canonical
line.

## Maven Central Activation

The first phase 2 expansion surface is:

```text
maven_central_artifact_metadata
```

It is activated only for the narrow Maven Central artifact metadata profile
defined in:

```text
governance/phase2_maven_central_artifact_metadata_dossier.md
```

The activation does not admit Maven snapshots, classifiers, dependency graphs,
search APIs, third-party indexes, authenticated sources, or non-Central Maven
repositories.

## crates.io Activation

The second phase 2 expansion surface is:

```text
crates_io_package_index_metadata
```

It is activated only for the narrow crates.io sparse index entry profile
defined in:

```text
governance/phase2_crates_io_package_index_metadata_dossier.md
```

The activation does not admit crate archive body hashing, crates.io API
metadata, GitHub repository metadata, downloads, ownership data, private
registries, authenticated endpoints, or local Cargo caches.

## Phase 2 Promise

RegistryOps phase 2 preserves the phase 1 proof chain while widening the active
observation surface.

It continues to prove what RegistryOps observed publicly, when it observed it,
and which deterministic observed-state profile was committed by each new
observation event through `observable_fingerprint`.

Phase 2 does not claim to model the full software supply chain, all Maven
repositories, or every possible artifact variant.

## Completion Rule

Phase 2 is considered correctly activated when:

- `maven_central_artifact_metadata` and
  `crates_io_package_index_metadata` are present in the active taxonomy
- their `asset_ref` and `source_ref` rules are executable
- the canonical observer can admit events for both phase 2 expansion surfaces
- the publication line starts at `snapshots/phase2-000001/`
- `current/` references the phase 2 line
- the public proof chain remains valid from journal to Merkle root to OTS
- phase 1 snapshots remain preserved as prior canonical history
