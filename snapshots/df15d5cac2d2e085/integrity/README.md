# Integrity & Verifiability

This registry is append-only and publishes verifiable artifacts.

## What is published
- `integrity/integrity.json`: SHA-256 of the full journal file + counts.
- `integrity/daily_roots/`: one Merkle root per UTC day (Daily Merkle Root Record).

## Daily Merkle Root (DMRR)
For each UTC day, events are:
1) filtered by `observed_at` date (UTC)
2) sorted by `event_id`
3) serialized as canonical JSON (sorted keys, UTF-8, no whitespace)
4) hashed with SHA-256 to form Merkle leaves
5) combined pairwise (duplicate last if odd) until one root remains

A third party can recompute the same root from the public `journal/events.jsonl`.
