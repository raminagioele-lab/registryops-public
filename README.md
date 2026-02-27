# RegistryOps Public Registry

This repository contains the public, append-only, verifiable surface of RegistryOps.

## Purpose

RegistryOps is a deterministic temporal registry that:

- Observes public API surfaces
- Emits append-only events
- Replays aggregated state deterministically
- Publishes verifiable public artifacts
- Never stores personal data
- Never performs ranking, scoring, or accusation

---

## Structure

registry/
  current/
    journal/events.jsonl
    state/state.json
    integrity/
    schemas/
    taxonomy/
    governance/
  snapshots/<publication_id>/

- `current/` → latest official publication
- `snapshots/` → immutable historical publications

---

## Integrity Model

Each publication includes:

- SHA-256 hash of full journal
- Daily Merkle Roots (DMRR)
- Canonical JSON serialization
- Deterministic replayable state

A third party can:

1. Recompute SHA-256 of `journal/events.jsonl`
2. Recompute daily Merkle roots
3. Verify append-only behavior
4. Verify snapshot immutability

---

## Guarantees

- Append-only journal
- Deterministic state replay
- No destructive mutation
- No private data
- Public verifiability

---

## Non-Goals

- No user accounts
- No scoring or ranking
- No legal accusation
- No moderation system

This repository is read-only infrastructure.
