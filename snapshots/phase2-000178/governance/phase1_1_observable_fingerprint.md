# RegistryOps Phase 1.1 Observable Fingerprint

## Status

This document defines the phase 1.1 public proof extension for RegistryOps.

It is normative for new observation events admitted after the phase 1.1
transition.

It does not rewrite, reinterpret, or invalidate phase 1 events already
published before the transition.

## Purpose

Phase 1 proved that a minimal public event was appended to the RegistryOps
journal and anchored through the publication proof chain.

Phase 1.1 strengthens that proof by adding a public fingerprint of the exact
observed-state profile behind each new observation event.

This allows a third party to verify not only that an event was recorded, but
also which deterministic public-state profile was committed by that event.

## Canonical Field

The phase 1.1 field is:

- `observable_fingerprint`

It is a lowercase SHA-256 hexadecimal digest.

It is required for new events whose `event_type` is one of:

- `first_seen`
- `reobserved`
- `state_changed`

It is not part of `event_id` generation.

The canonical `event_id` formula remains unchanged and continues to use only:

- `asset_ref`
- `surface_type`
- `event_type`
- `observed_at`
- `source_ref`

## Fingerprint Construction

For each surface, RegistryOps constructs a canonical observed-state profile.

The `observable_fingerprint` is:

```text
sha256(canonical_json_bytes(observed_state))
```

where `canonical_json_bytes` serializes JSON with sorted keys, compact
separators, UTF-8 encoding, and no ASCII escaping.

The observed-state profile is not published as canonical content. The public
journal publishes only its digest.

## Surface Profiles

### `oci_manifest`

The observed-state profile contains:

- `docker_content_digest`
- `content_type`
- `etag`
- `content_length`

### `npm_package_metadata`

The observed-state profile contains:

- `name`
- `version`
- `deprecated`
- `dist.shasum`
- `dist.integrity`
- `dist.tarball`

### `pypi_release_metadata`

The observed-state profile contains:

- `project`
- `version`
- `yanked`
- `yanked_reason`
- `files`

Each file entry contains:

- `filename`
- `packagetype`
- `python_version`
- `yanked`
- `digests.sha256`
- `upload_time_iso_8601`
- `url`

File entries are sorted deterministically by `filename`, then `packagetype`.

### `ietf_internet_draft`

The observed-state profile contains:

- `content_sha256`
- `content_length`
- `etag`
- `last_modified`

## Public Proof Consequence

From the phase 1.1 transition onward, each new observation event line committed
to `journal/events.jsonl` includes `observable_fingerprint`.

Because the Merkle root is calculated from the exact journal lines, the
snapshot proof commits both the event identity fields and the public
observed-state fingerprint.

Operational receipts may continue to preserve additional local observation
context, but they are no longer the only place where the observed-state digest
exists.

## Transition Rule

Historical phase 1 events remain canonical without `observable_fingerprint`.

Once the first phase 1.1 observation event with `observable_fingerprint` appears
in the journal, subsequent observation events must also include a valid
`observable_fingerprint`.

This creates a clean forward-only transition while preserving the validity of
the existing canonical history.
