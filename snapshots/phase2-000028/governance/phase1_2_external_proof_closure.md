# RegistryOps Phase 1.2 External Proof Closure

## Status

This document defines the phase 1.2 external proof closure rule for
RegistryOps.

It is normative for official phase 1 operation after the phase 1.2 transition.

It does not rewrite, reinterpret, or invalidate earlier phase 1 or phase 1.1
snapshots.

## Purpose

Phase 1 established the canonical publication and Merkle-root proof chain.

Phase 1.1 strengthened public events with `observable_fingerprint`.

Phase 1.2 closes the operational gap between a published snapshot and its
external OpenTimestamps proof attempt.

The goal is to ensure that `pending_ots` means a proof could not yet be
obtained or completed, not that the official runner was missing the OTS tool.

## Official OTS CLI Requirement

Official RegistryOps operation must provide the OpenTimestamps CLI command:

- `ots`

The official workflow must install the `opentimestamps-client` package and
verify the availability of `ots` before running the canonical operation
pipeline.

If the official runner cannot provide `ots`, the operation must fail rather
than silently publishing or maintaining a snapshot as `pending_ots` because of
tooling absence.

## Pending OTS Semantics

`pending_ots` remains a valid public proof status.

It is valid when:

- the snapshot is canonical and published
- the Merkle root and anchor payload are published
- no real `anchor.ots` proof is available yet
- the absence of `anchor.ots` is accurately represented in
  `integrity/proof_status.json`

It must not be used to hide an official environment misconfiguration such as a
missing `ots` command.

## Calendar Failure Semantics

If `ots` is available but remote calendar stamping or upgrade cannot complete,
the snapshot may remain `pending_ots`.

This is an external proof availability condition, not a local tooling failure.

RegistryOps must keep retrying proof attachment or upgrade on later official
cycles.

## Verification Progression

The phase 1.2 proof progression is:

1. `pending_ots`
2. `ots_present_unverified`
3. `verified`

`verified` remains reserved for snapshots whose OTS proof has been checked
through a valid Bitcoin anchoring path.

## Publication Rule

From phase 1.2 onward, canonical publications expose this document in:

`governance/phase1_2_external_proof_closure.md`

Snapshots published before phase 1.2 remain historically valid without this
file.

## Compliance Rule

An official phase 1.2 RegistryOps operation is compliant only if:

- the official operation workflow installs `opentimestamps-client`
- the official operation workflow confirms that `ots` is executable
- missing `ots` is treated as a pipeline failure
- real OTS calendar unavailability may still produce `pending_ots`
- proof statuses continue to follow the public proof status contract
