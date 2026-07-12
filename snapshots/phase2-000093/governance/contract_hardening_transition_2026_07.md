# RegistryOps Contract Hardening Transition - July 2026

## Status

This document is normative for every publication whose manifest declares:

`contract_profile = registryops-contract-2026-07`

It establishes a prospective compatibility boundary. It does not rewrite or
silently repair any event, snapshot, proof, schema, or derived state published
before this profile.

## Audited Baseline

The transition was prepared from the public state identified by:

- canonical publication: `phase2-000091`
- canonical event count: `491`
- canonical journal SHA-256:
  `2a50cf836df5bc9c6af9b84db489f6739b832fcbd08f86690b964d7f7addf0fc`
- core baseline commit: `30b5f97dff6055a03c408105ac9f55e8c1e54b4d`
- mirror baseline commit: `2d01d7f80f5dad10536da68cc38f2bf8272a753c`

The immutability ledger records the exact tree digest of every snapshot that
exists when the first hardened publication is finalized. Earlier snapshots are
marked as a legacy baseline. Hardened snapshots are protected from their first
publication.

## Historical Disclosure

The pre-transition line remains canonical history, but it carries disclosed
contract limitations:

- many historical copies of `proof_status.schema.json` are not valid JSON
- proof maturation modified some snapshot directories after first publication
- the implementation used journal line order while an older constitutional
  text required an `event_id` tie-break for equal timestamps
- historical derived states contain two fields outside the superior state model
- the first 109 events do not publish `observable_fingerprint`; 108 related
  fingerprints remain available only in operational receipts
- no historical snapshot is represented as Bitcoin verified at this transition

These facts must remain visible. They must not be corrected by editing the
historical snapshots.

## Immutable Snapshot Rule

Once a hardened snapshot is finalized, every file below
`snapshots/<publication_id>/` is immutable.

The immutable snapshot ledger is published at `immutability_ledger.json`.

Any missing snapshot, unregistered snapshot, or tree digest mismatch is a
blocking contract failure. Release automation must reject a change that would
remove or modify an existing snapshot.

## Evolving Proof Attestations

OpenTimestamps proofs may mature after snapshot publication. That maturation
must never modify the snapshot.

Each subsequent proof state is published as an immutable revision below:

`attestations/<publication_id>/<revision_id>/`

Each revision contains `anchor.ots` and `attestation_manifest.json`.
`latest.json` is a mutable convenience pointer to the newest immutable
revision. It is not itself a citation unit. A strong citation names both the
snapshot publication id and the attestation revision id.

The proof status stored inside a snapshot describes its status at publication
time. The effective current proof status is the status of the latest valid
attestation revision when one exists, otherwise the snapshot status.

## Canonical Ordering Compatibility Profile

The exact physical order of non-empty lines in `journal/events.jsonl` is the
canonical event order for the complete RegistryOps history.

`observed_at` must remain non-decreasing. Equal timestamps are ordered by their
committed journal line positions. `event_id` remains the stable event identity
but is not a secondary sorting key.

This profile resolves the historical conflict between the implemented
append-only single-writer journal and the former tie-break text. No historical
line may be reordered.

## Derived State Contract

Hardened publications expose `schemas/state.schema.json`. Their derived
`state/state.json` must contain exactly the eight fields authorized by
`ops/aggregated_state_model.md` and must equal a deterministic replay of the
canonical journal.

## Contract Validation Gate

Every hardened publication must pass all of the following before release:

- every published JSON Schema parses and passes the Draft 2020-12 metaschema
- every event, manifest, proof status, state, and proof attestation validates
  against its published schema
- the derived state exactly matches deterministic journal replay
- journal SHA-256, event count, Merkle root, and anchor payload are coherent
- the complete snapshot sequence remains a monotone prefix chain
- the immutability ledger covers every canonical snapshot
- every existing snapshot and attestation revision remains byte-identical

The public mirror distributes `verify_registryops.py`, a self-contained
read-only verifier for these rules. It must not require access to the private
core repository or to any secret. Its output is a verification result derived
from the public artifacts, not an additional source of truth.

## Dashboard Semantics

RegistryOps must expose three independent top-level assessments:

- Operational Health
- Contract Compliance
- Proof Assurance

A green operational status must never imply green contract compliance or green
proof assurance.

## Claim Boundary

Before Contract Compliance and Proof Assurance are both green, RegistryOps may
be described as operational, stable, append-only, and internally coherent. It
must not be described as fully contract-conformant, fully immutable across its
entire historical line, or externally verified through Bitcoin.
