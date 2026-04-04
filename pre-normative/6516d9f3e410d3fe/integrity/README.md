# Integrity & Verifiability

This registry is append-only and publishes verifiable artifacts.

## What is published
- `integrity/integrity.json`: SHA-256 of the full journal file, counts, and the global journal Merkle root.
- `integrity/daily/`: one daily proof manifest per UTC day.
- `integrity/daily_roots/`: legacy daily Merkle records retained for compatibility.
- `integrity/anchors/`: OpenTimestamps payloads and `.ots` proofs when available.

## Daily Merkle rule
For each UTC day, events are:
1. filtered by `observed_at` date (UTC)
2. sorted by `(observed_at, event_id)`
3. serialized as canonical JSON (sorted keys, UTF-8, no whitespace)
4. hashed with SHA-256 to form Merkle leaves
5. combined pairwise (duplicate last leaf if odd) until one root remains

A third party can recompute the same root from the public `journal/events.jsonl`.
