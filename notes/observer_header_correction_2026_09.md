# September 2026 Header Collection Correction

Documentary operational notice, outside the canonical snapshot contract.
This notice is not a Merkle-anchored event or an amendment to published snapshots.

Collector revision `registryops-observer-header-correction-2026-09` corrects
case-sensitive HTTP header lookup for OCI and the optional IETF headers.
HTTP field names are case-insensitive ([RFC 9110 section 5.1](https://www.rfc-editor.org/rfc/rfc9110.html#name-field-names)).
The journal schema, fingerprint serialization, event taxonomy, source grammars,
watchlist and cadence are unchanged.

From the first observation by this revision, a successful OCI observation
requires a supported digest (`sha256` with 64 lowercase hex digits or `sha512`
with 128), an admissible manifest/index media type and a positive content
length. Missing or malformed essential values are operational failures,
not evidence of withdrawal and not successful unchanged observations.
Other targets continue independently.

The retained nginx 1.27.4 legacy fingerprint
`7e29d05e4a45d73fdf099fad3c927db215dec32439cd3b04faea78211644dc3f`
commits `docker_content_digest=null` and `etag=null`. It cannot establish the
historical tag-to-digest mapping. Existing snapshots and events remain exactly
as published, at that limited assurance level. A digest retrieved today must
never be inserted into the past.

Recovering previously ignored headers can change the observed profile even
when no upstream content change is established. The first differing profile
still follows the existing `state_changed` rule; it is a change of the collected
profile, not by itself proof of a registry mutation. The observer records the
collector revision and `collector_header_correction_boundary` interpretation
in its operational cycle report when leaving the known legacy baselines.

The corresponding IETF baseline for
`draft-ietf-httpbis-incremental-00` is
`dcca62a7abe7f5ccb8fbc7c2e0c98de5f604af22e80b675a48ebb5cd29e12f18`.
Its body SHA-256 was retained; recovering an ETag or Last-Modified value must
not be confused with proof that the draft body changed.

The existing governance documents are retained byte-for-byte because they
also belong to a frozen candidate review baseline. This separate notice
neither changes that baseline nor activates candidate Evidence Objects.
External review and Bitcoin verification remain separate requirements.
