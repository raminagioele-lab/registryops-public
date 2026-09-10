# RegistryOps Phase 2 Surface Expansion Framework

## Status

This document defines the phase 2 expansion framework and records the first
phase 2 surface activation.

The framework itself remains the rule for future expansion. The active phase 2
scope is defined in `ops/phase2_scope.md`.

## Purpose

Phase 2 must expand RegistryOps only after phase 1 proof closure remains
stable.

The goal is to identify public surfaces whose temporal history is likely to
become difficult, expensive, or impossible to reconstruct later if RegistryOps
does not observe them continuously.

## Activation Gate

A candidate surface may become active only after all of the following are
closed:

- canonical `surface_type`
- canonical `asset_ref` grammar
- canonical `source_ref` grammar
- allowed public source hosts
- observed-state profile
- `observable_fingerprint` construction
- event classification rules
- cadence rule
- non-personal-data review
- public verification path
- operational rate and availability policy

Until those items are closed, a candidate remains non-active.

## Selection Criteria

Candidate surfaces should be scored against:

- public accessibility without authentication
- stable public identifiers
- natural versioning or temporal state
- meaningful risk of later historical loss
- low personal-data exposure
- strong primary-source observability
- deterministic observed-state profile
- compatibility with append-only public proof
- ecosystem importance
- under-observation by independent temporal registries

## Initial Non-Active Shortlist

The following candidates have high phase 2 potential.

### Maven Central artifact metadata

Status:

- active in phase 2 as `maven_central_artifact_metadata`

Rationale:

- high software supply-chain importance
- stable coordinates: group, artifact, version
- public metadata and checksum artifacts
- strong fit for release persistence and artifact-state proof

Primary public references:

- `https://repo1.maven.org/maven2/`
- `https://central.sonatype.com/`

Candidate dossier:

- `ops/phase2_maven_central_artifact_metadata_dossier.md`

### crates.io package index metadata

Status:

- active in phase 2 as `crates_io_package_index_metadata`

Rationale:

- high Rust ecosystem importance
- public package index
- stable crate/version metadata
- useful for observing yanks, checksums, dependencies, and index evolution

Primary public references:

- `https://index.crates.io/`
- `https://github.com/rust-lang/crates.io-index`

Activation dossier:

- `ops/phase2_crates_io_package_index_metadata_dossier.md`

### Go module proxy and checksum database metadata

Status:

- non-active candidate

Rationale:

- high Go ecosystem importance
- public proxy protocol
- deterministic module/version endpoints
- strong fit for observing module version availability over time

Primary public reference:

- `https://go.dev/ref/mod`

### GitHub release and tag metadata

Status:

- non-active candidate

Rationale:

- very high open-source distribution importance
- public release metadata can change or disappear
- tags and release assets are central to software provenance
- requires careful rate-limit and authentication-free policy review

Primary public reference:

- `https://docs.github.com/rest/releases/releases`

### Sigstore Rekor transparency log metadata

Status:

- non-active candidate

Rationale:

- high software supply-chain proof importance
- public transparency log and API
- already append-only, but valuable as an independently timestamped
  meta-observation target
- requires careful scope design to avoid duplicating Rekor rather than
  observing its public log state

Primary public reference:

- `https://docs.sigstore.dev/logging/overview/`

### Certificate Transparency log state

Status:

- non-active candidate

Rationale:

- globally important public transparency infrastructure
- append-only and publicly auditable
- already widely monitored, so it may be less differentiating than package
  ecosystem surfaces
- useful as a later benchmark for RegistryOps proof and log-monitoring
  capabilities

Primary public reference:

- `https://certificate.transparency.dev/logs/`

## Recommended Phase 2 Order

The recommended order for deeper phase 2 evaluation is:

1. crates.io package index metadata
2. Go module proxy and checksum database metadata
3. GitHub release and tag metadata
4. Sigstore Rekor transparency log metadata
5. Certificate Transparency log state

Maven Central was the first item in the original recommended order and is now
the first active phase 2 expansion surface.

## Non-Activation Rule

No future phase 2 observer may be implemented until the target surface has a
closed surface dossier.

Each dossier must include:

- canonical references
- concrete examples
- exact grammar
- exact observed-state profile
- expected event transitions
- expected failure modes
- public verification story
- operational cadence
- rate-limit constraints

## Phase 2 Posture

Phase 2 should widen RegistryOps only after the phase 1 line remains stable,
publicly verifiable, and operationally quiet.

Breadth must not weaken the phase 1 proof chain.
