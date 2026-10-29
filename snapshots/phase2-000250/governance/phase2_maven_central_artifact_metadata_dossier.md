# RegistryOps Phase 2 Candidate Dossier: Maven Central Artifact Metadata

## Status

This document defines the phase 2 Maven Central surface dossier.

It is normative for `maven_central_artifact_metadata` after the phase 2
activation snapshot.

It does not rewrite, reinterpret, or invalidate prior phase 1 snapshots.

The active `surface_type` defined by this dossier is:

- `maven_central_artifact_metadata`

This value is admissible in the canonical event model from `phase2-000001`
onward.

## Purpose

The purpose of this surface is to observe the public temporal state of Maven
Central release artifacts.

Maven Central is a major software supply-chain distribution surface. Its
artifact coordinates are stable, public, widely consumed, and naturally suited
to long-term temporal observation.

RegistryOps phase 2 should observe this surface only in a narrow and
deterministic form: public release artifact metadata, checksum sidecars, POM
state, and Maven repository metadata that can be reconstructed by a third
party from primary public sources.

## Primary References

The dossier is based on the following primary public references:

- Apache Maven repository layout:
  `https://maven.apache.org/repositories/layout.html`
- Apache Maven artifacts:
  `https://maven.apache.org/repositories/artifacts.html`
- Apache Maven metadata:
  `https://maven.apache.org/repositories/metadata.html`
- Apache Maven repository metadata model:
  `https://maven.apache.org/ref/3.9.9/maven-repository-metadata/index.html`
- Sonatype Central consumption documentation:
  `https://central.sonatype.org/consume/`

## Active Boundary

The initial phase 2 Maven Central surface is limited to release artifacts
served by Maven Central's public repository layout.

It includes:

- non-SNAPSHOT release coordinates
- unclassified primary artifact resources
- explicit artifact extension
- the public artifact resource
- the corresponding POM resource
- the group/artifact `maven-metadata.xml` resource
- checksum sidecar resources for the artifact and the POM
- optional detached signature resource state

It excludes:

- SNAPSHOT versions
- classifier artifacts
- search APIs
- dependency graph reconstruction
- vulnerability, popularity, license, or quality metadata
- third-party indexes
- authenticated endpoints
- non-Central repositories
- mirrors treated as independent sources

These exclusions are intentional. They keep the first Maven Central surface
small enough to verify publicly and stable enough to operate without weakening
the inherited proof chain.

## Canonical Surface Type

The canonical `surface_type` is:

```text
maven_central_artifact_metadata
```

No other Maven-related `surface_type` is introduced by this dossier.

Future surfaces such as Maven classifiers, Maven snapshots, Maven dependency
graphs, or Central Search metadata must be specified separately.

## Canonical Asset Reference

The canonical `asset_ref` grammar is:

```text
<group_id>:<artifact_id>:<version>:<extension>
```

Examples:

```text
org.apache.commons:commons-lang3:3.14.0:jar
com.google.guava:guava:33.1.0-jre:jar
org.apache.maven:maven-parent:42:pom
```

Field rules:

- `group_id` is the Maven groupId as published, without URL encoding.
- `artifact_id` is the Maven artifactId as published.
- `version` is the Maven release version as published.
- `extension` is the explicit artifact extension being observed.
- field separators are literal colon characters.
- fields must not contain `/`, whitespace, query syntax, fragment syntax, or
  empty values.
- `version` must not end with `-SNAPSHOT`.
- classifier artifacts are not admissible in this initial surface.

The recommended validation pattern is:

```text
^[A-Za-z0-9_.-]+:[A-Za-z0-9_.-]+:[A-Za-z0-9][A-Za-z0-9_.+~-]*:[A-Za-z0-9][A-Za-z0-9_.-]*$
```

This pattern is intentionally stricter than every historical Maven edge case.
If a valuable Central coordinate falls outside this grammar, it should be
handled by a later governed extension rather than by weakening the initial
surface.

## Canonical Source Reference

The canonical `source_ref` grammar is:

```text
https://repo1.maven.org/maven2/<group_path>/<artifact_id>/<version>/<artifact_id>-<version>.<extension>
```

where:

- `group_path` is `group_id` with `.` replaced by `/`.
- `artifact_id`, `version`, and `extension` are copied exactly from
  `asset_ref`.

Example:

```text
https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.14.0/commons-lang3-3.14.0.jar
```

The only allowed public source host for the initial surface is:

```text
repo1.maven.org
```

The `source_ref` must:

- use HTTPS
- be absolute
- contain no username or password
- contain no query string
- contain no fragment
- point to the primary public artifact resource for the asset

Equivalent Maven Central access paths must not be accepted during initial
activation. This avoids two URLs representing the same observed object.

## Associated Public Resources

For a valid `asset_ref`, RegistryOps derives the following associated resources
deterministically.

The POM resource is:

```text
https://repo1.maven.org/maven2/<group_path>/<artifact_id>/<version>/<artifact_id>-<version>.pom
```

The group/artifact metadata resource is:

```text
https://repo1.maven.org/maven2/<group_path>/<artifact_id>/maven-metadata.xml
```

Checksum sidecars are probed for both the artifact resource and the POM
resource by appending the following suffixes in this exact order:

```text
.sha1
.md5
.sha256
.sha512
```

The detached signature resource is probed by appending:

```text
.asc
```

Missing checksum or signature resources are recorded as public absence, not as
observer failure, unless the missing resource is later made mandatory by a
separate normative activation.

## Observed-State Profile

The observed-state profile is the canonical public state committed through
`observable_fingerprint`.

It contains:

- `surface_type`
- `asset_ref`
- `source_ref`
- `artifact`
- `pom`
- `ga_metadata`

The `artifact` object contains:

- `url`
- `http_status`
- `content_length`
- `etag`
- `last_modified`
- `checksum_sidecars`
- `signature`

The artifact body is not fetched or hashed in the initial surface.
The surface observes Maven Central's public artifact metadata and checksum
sidecars, not the full binary bytes.

The `pom` object contains:

- `url`
- `http_status`
- `content_sha256`
- `content_length`
- `checksum_sidecars`
- `signature`

The POM body is fetched because it is a small public metadata artifact and is
central to Maven coordinate verification.

The `ga_metadata` object contains:

- `url`
- `http_status`
- `content_sha256`
- `groupId`
- `artifactId`
- `latest`
- `release`
- `lastUpdated`
- `versions`
- `target_version_present`

The `versions` value is the exact ordered version list parsed from
`metadata/versioning/versions/*`.

## Normalization Rules

The observer must normalize the observed-state profile as follows:

- JSON is serialized with sorted keys, compact separators, UTF-8 encoding, and
  no ASCII escaping.
- XML bodies are hashed as exact received bytes. RegistryOps does not apply XML
  canonicalization.
- checksum sidecar values are trimmed of leading and trailing ASCII whitespace.
- hexadecimal checksum sidecar values are lowercased.
- absent optional resources are represented explicitly with their HTTP status
  and a `null` value.
- absent HTTP headers are represented as `null`.
- response date, server, cache, CDN, and transfer headers are excluded from the
  profile.

## Observable Fingerprint

The `observable_fingerprint` is:

```text
sha256(canonical_json_bytes(observed_state))
```

The fingerprint commits to the public metadata profile behind the event.

It does not claim to be an independent cryptographic hash of the full artifact
binary unless a later surface explicitly adds full artifact-body hashing.

## Event Classification Rules

The surface uses the existing RegistryOps event taxonomy.

`first_seen` is emitted when a target artifact is successfully observed for the
first time and the artifact resource, POM resource, and group/artifact metadata
resource are all publicly available.

`reobserved` is emitted when the same observed-state fingerprint is observed in
a later admissible cycle.

`state_changed` is emitted when the target remains publicly available but the
observed-state fingerprint changes.

`withdrawn` is emitted when a previously observed artifact resource becomes
publicly absent through an authoritative `404` or `410` response.

`unreachable` is emitted when RegistryOps cannot make a reliable public
determination because of timeout, DNS failure, TLS failure, `429`, or `5xx`
responses.

`revoked`, `replaced`, and `expired` are not emitted by the initial Maven
Central surface unless a later normative rule defines an authoritative Maven
Central signal for those states.

## Cadence Rule

The default Maven Central cadence is:

- observe enabled Maven Central targets at least once every 24 hours
- admit an unchanged `reobserved` event only when at least 24 hours have passed
  since the last canonical observation of the same state for the same asset
- admit `state_changed`, `withdrawn`, or `unreachable` as soon as detected in a
  distinct observation cycle

This matches the phase 1 posture and avoids artificial density.

## Operational Rate And Availability Policy

The initial observer must be conservative.

Per target and per cycle, it may perform only the requests required to build
the observed-state profile.

The initial operational ceiling is:

- at most 13 public HTTP requests per target per cycle
- at most 1 request per second to `repo1.maven.org`
- respect `Retry-After` when present
- treat `429` as `unreachable`, not as artifact withdrawal
- use a deterministic RegistryOps user agent
- avoid authenticated access
- avoid parallel bursts against Maven Central

The observer must not depend on Central Search, browser scraping, third-party
indexes, or local Maven caches.

## Non-Personal-Data Review

The surface is acceptable from a non-personal-data perspective only
under the following constraint:

- public events publish only `asset_ref`, `surface_type`, `event_type`,
  `observed_at`, `source_ref`, and `observable_fingerprint`.

The public event must not publish POM developer names, emails, URLs, SCM
details, or organization fields.

The observed-state profile may hash the POM bytes, but the POM content itself
must not be copied into the canonical public journal.

## Public Verification Path

A third party can verify a Maven Central event by:

1. Reading the event from `journal/events.jsonl`.
2. Reconstructing the Maven Central URLs from `asset_ref` and `source_ref`.
3. Fetching the public artifact metadata, POM, checksum sidecars, detached
   signature state, and group/artifact `maven-metadata.xml`.
4. Building the observed-state profile according to this dossier.
5. Recomputing `observable_fingerprint`.
6. Checking that the fingerprint matches the event line.
7. Verifying that the event line is included in the snapshot journal.
8. Recomputing the snapshot Merkle root from `journal/events.jsonl`.
9. Checking the root against `integrity/merkle_root.txt`.
10. Checking the OTS proof status and external anchor according to the public
    RegistryOps proof contract.

This proves what Maven Central public metadata state RegistryOps committed at
the observation time. It does not prove that Maven Central never served a
different state to another observer.

## Failure Modes

The initial implementation must explicitly handle:

- artifact `404` before first observation
- artifact `404` after prior successful observation
- POM missing while artifact exists
- group/artifact metadata missing while artifact exists
- checksum sidecar missing
- malformed checksum sidecar content
- malformed XML in POM or `maven-metadata.xml`
- CDN timeout
- DNS failure
- TLS failure
- `429` rate limiting
- `5xx` server responses
- unexpected redirects

Unexpected redirects must not silently change the canonical `source_ref`.

## Candidate Examples

Good candidate targets for implementation testing are stable, widely known,
non-SNAPSHOT release artifacts, for example:

```text
org.apache.commons:commons-lang3:3.14.0:jar
com.google.guava:guava:33.1.0-jre:jar
org.apache.maven:maven-parent:42:pom
```

These examples do not define the official watchlist by themselves.

## Activation Checklist

Before this surface was activated, RegistryOps had to add and test:

- taxonomy entry for `maven_central_artifact_metadata`
- surface rules entry with the grammar defined here
- event schema compatibility for the new surface
- Maven Central observer implementation
- deterministic observed-state profile builder
- fingerprint tests using fixed fixtures
- source URL reconstruction tests
- event classification tests
- rate-limit behavior tests
- watchlist entries for selected Maven Central targets
- operational monitor coverage
- public governance file in new snapshots

Activation is represented by the phase 2 normative change and the first
`phase2-*` publication.

## Candidate Observation Mode

RegistryOps may run a non-canonical candidate observer for this surface before
activation.

The candidate observer is:

```text
registry/scripts/observe_maven_central_candidate.py
```

Its candidate watchlist is:

```text
observation/phase2_maven_central_candidates.json
```

This mode writes only local operational candidate receipts under:

```text
ops_state/phase2/
```

It must not write to:

- `registry/data/events.jsonl`
- `registry/ingestion/observation_receipts.jsonl`
- `registry/ingestion/observation_cycles.jsonl`
- `registry/taxonomy/`
- `registry/schemas/`

The candidate observer is useful for validating real Maven Central behavior,
fingerprint stability, request volume, checksum availability, metadata parsing,
and failure handling before official phase 2 activation.

Candidate observations are evidence for design validation. They are not
canonical RegistryOps events.

## Phase 2 Recommendation

This surface is the first active phase 2 implementation target.

It has high ecosystem value, strong public reconstructibility, stable
identifiers, clear checksum metadata, and low personal-data exposure when only
fingerprints are published.

It became admissible only after candidate observation demonstrated stable
fingerprints across multiple observation cycles.
