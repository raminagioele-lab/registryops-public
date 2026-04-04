# publication_governance_v1.md
Version: v1
Status: Normative
Scope: Day 18 — Governance Hardening & Publication Policy Lock

---

## 1. Purpose

This document defines the governance rules for publishing a public, no-login temporal registry:
- Append-only event log as the single source of truth
- Deterministic, replayable aggregated state
- Public read-only surface
- No personal data (NOPII)
- No accusation, scoring, ranking, or person-targeted functionality
- Non-destructive evolution only

---

## 2. Roles and Decision Authority

### 2.1 Maintainers
Maintainers are responsible for:
- Approving changes to schemas, event types, taxonomy, and publication process
- Executing official publications
- Ensuring invariant compliance before and after release

### 2.2 Change Approval Rule
A change is approved only if:
- It is non-destructive
- It preserves replay determinism
- It preserves NOPII constraints
- It preserves the public read-only model
- It introduces no accusation/scoring/ranking logic

All approved changes MUST be recorded in a versioned decision log (see Section 8).

---

## 3. Immutable Core Invariants (Non-Negotiable)

The following MUST always hold:

1) Append-only events: no UPDATE/DELETE, no rewrites  
2) Deterministic replay: same events → same state (except timestamps like generated_at)  
3) No personal data: no direct identifiers (names, emails, phone numbers, addresses, user IDs)  
4) Neutral registry: no accusations, scoring, rankings, blacklists, or person-targeted outputs  
5) Public access without login: read-only distribution  
6) Versioned, non-destructive evolution only

Any change violating these invariants is forbidden.

---

## 4. Versioning Policy

### 4.1 Registry Version
`registry_version` identifies the overall product release line (e.g., "1.0").

It MUST NOT change for minor internal refactors that do not affect public artifacts or schemas.

### 4.2 Schema Versions
- `schema_event_v1.json` and `schema_state_v1.json` are versioned artifacts.
- Backward-incompatible changes require a new version (v2, v3, ...).
- Old schema versions MUST remain accessible publicly once published.

### 4.3 State Version
`state_version` identifies the semantics of the aggregated state computation.

A new state computation that changes meaning or fields MUST bump `state_version` (e.g., v2).

---

## 5. Non-Destructive Evolution Rule

Changes MUST be additive or parallelized, never destructive:

Allowed:
- Add a new optional field with safe defaults
- Add a new event_type (taxonomy versioned)
- Add a new state_version published in parallel

Forbidden:
- Remove or rename existing public fields without maintaining the old version
- Rewrite historical events
- Replace published artifacts in a way that breaks historical verification

---

## 6. Publication Process (Normative)

An official publication MUST follow this pipeline:

1) Copy canonical journal (read-only) into isolated build directory  
2) Validate schema + NOPII rules  
3) Deterministic full replay to generate state  
4) Compute integrity hash of events.jsonl (SHA256)  
5) Generate public_manifest.json  
6) Atomic swap build → public using filesystem rename semantics  
7) Freeze public directory permissions to read-only

Direct writes into /public are forbidden.

---

## 7. Migration Policy

When introducing a new schema or state version:

- Publish the new version alongside the old one
- Keep older versions accessible (schemas, taxonomy, governance docs)
- Do not break verification of previously published snapshots
- Provide a short migration note explaining:
  - what changed
  - why it changed
  - compatibility implications

No automated rewriting of historical logs is permitted.

---

## 8. Decision Log Requirement

All governance-relevant decisions MUST be recorded as a versioned file:

- Location: `ops/decision_log.md`
- Entries MUST include:
  - date (UTC)
  - change summary
  - versions affected (schema/state/taxonomy)
  - invariant impact statement (explicit: "no change" or "additive only")
  - approver identifier (role-based, not personal data)

The decision log MUST NOT contain personal data.

---

## 9. Public Availability

This governance document MUST be published on the public surface:

Target path:
- `public/governance/publication_governance_v1.md`

Once published, it becomes part of the audit trail.

---

END OF FILE