#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, urlparse

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError
except Exception:  # pragma: no cover - reported explicitly by the CLI
    Draft202012Validator = None
    SchemaError = ValueError
    ValidationError = ValueError


HARDENED_CONTRACT_PROFILE = "registryops-contract-2026-07"
SNAPSHOT_RE = re.compile(r"^phase[12]-\d{6}$")
REVISION_RE = re.compile(r"^r(\d{6})$")
OBSERVATION_EVENT_TYPES = {"first_seen", "reobserved", "state_changed"}
PRIOR_OBSERVATION_REQUIRED_TYPES = {
    "state_changed",
    "withdrawn",
    "revoked",
    "replaced",
    "expired",
}
REOBSERVE_INTERVAL_SECONDS = 24 * 60 * 60
CANONICAL_EVENT_FIELDS = (
    "event_id",
    "asset_ref",
    "surface_type",
    "event_type",
    "observed_at",
    "source_ref",
)


class VerificationError(ValueError):
    pass


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise VerificationError(f"Cannot parse JSON {path}: {exc}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise VerificationError(f"Missing directory: {root}")
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256_file(path)))
        digest.update(b"\n")
    return digest.hexdigest()


def compute_merkle_root(lines: list[str]) -> str:
    if not lines:
        return hashlib.sha256(b"").hexdigest()
    level = [hashlib.sha256(line.encode("utf-8")).digest() for line in lines]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            hashlib.sha256(level[index] + level[index + 1]).digest()
            for index in range(0, len(level), 2)
        ]
    return level[0].hex()


def parse_utc(value: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise VerificationError(f"Invalid canonical UTC timestamp: {value!r}")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception as exc:
        raise VerificationError(f"Invalid canonical UTC timestamp: {value!r}") from exc


def canonical_event_id(event: dict) -> str:
    material = "\n".join(
        event[field]
        for field in (
            "asset_ref",
            "surface_type",
            "event_type",
            "observed_at",
            "source_ref",
        )
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def canonical_event_line(event: dict) -> str:
    canonical = {field: event[field] for field in CANONICAL_EVENT_FIELDS}
    if "observable_fingerprint" in event:
        canonical["observable_fingerprint"] = event["observable_fingerprint"]
    return json.dumps(canonical, ensure_ascii=False, separators=(",", ":"))


def expected_source_ref(surface_type: str, asset_ref: str) -> str:
    if surface_type == "oci_manifest":
        registry_and_repository, tag = asset_ref.rsplit(":", 1)
        registry, repository = registry_and_repository.split("/", 1)
        return f"https://{registry}/v2/{repository}/manifests/{quote(tag, safe='._-~')}"
    if surface_type == "npm_package_metadata":
        split_index = asset_ref.rfind("@")
        package_name = asset_ref[:split_index]
        version = asset_ref[split_index + 1 :]
        return (
            f"https://registry.npmjs.org/{quote(package_name, safe='@')}/"
            f"{quote(version, safe='._-~+')}"
        )
    if surface_type == "pypi_release_metadata":
        project_name, version = asset_ref.split("==", 1)
        return f"https://pypi.org/pypi/{project_name}/{quote(version, safe='._-~+')}/json"
    if surface_type == "ietf_internet_draft":
        return f"https://www.ietf.org/archive/id/{asset_ref}.txt"
    if surface_type == "maven_central_artifact_metadata":
        group_id, artifact_id, version, extension = asset_ref.split(":", 3)
        group_path = "/".join(quote(part, safe="._-~+") for part in group_id.split("."))
        artifact_part = quote(artifact_id, safe="._-~+")
        version_part = quote(version, safe="._-~+")
        extension_part = quote(extension, safe="._-~+")
        return (
            "https://repo1.maven.org/maven2/"
            f"{group_path}/{artifact_part}/{version_part}/"
            f"{artifact_part}-{version_part}.{extension_part}"
        )
    if surface_type == "crates_io_package_index_metadata":
        crate_name = asset_ref.rsplit("@", 1)[0]
        if len(crate_name) == 1:
            index_path = f"1/{quote(crate_name, safe='')}"
        elif len(crate_name) == 2:
            index_path = f"2/{quote(crate_name, safe='')}"
        elif len(crate_name) == 3:
            index_path = f"3/{quote(crate_name[0], safe='')}/{quote(crate_name, safe='')}"
        else:
            index_path = (
                f"{quote(crate_name[0:2], safe='')}/"
                f"{quote(crate_name[2:4], safe='')}/"
                f"{quote(crate_name, safe='')}"
            )
        return f"https://index.crates.io/{index_path}"
    raise VerificationError(f"Unsupported surface_type: {surface_type}")


def validate_schema(schema_path: Path) -> dict:
    if Draft202012Validator is None:
        raise VerificationError("jsonschema is required to verify the hardened public contract")
    schema = load_json(schema_path)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise VerificationError(f"Invalid JSON Schema {schema_path}: {exc}") from exc
    return schema


def validate_instance(instance, schema: dict, label: str) -> None:
    try:
        Draft202012Validator(schema).validate(instance)
    except ValidationError as exc:
        location = "/".join(str(item) for item in exc.absolute_path) or "<root>"
        raise VerificationError(f"{label} violates its schema at {location}: {exc.message}") from exc


def read_journal(root: Path) -> tuple[list[str], list[dict]]:
    journal_path = root / "journal" / "events.jsonl"
    try:
        with journal_path.open("r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]
        events = [json.loads(line) for line in lines]
    except Exception as exc:
        raise VerificationError(f"Cannot parse canonical journal {journal_path}: {exc}") from exc
    if not all(isinstance(event, dict) for event in events):
        raise VerificationError(f"Canonical journal contains a non-object event: {journal_path}")
    return lines, events


def replay_state(events: list[dict], recomputed_at: str) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for event in events:
        grouped[(event["surface_type"], event["asset_ref"])].append(event)

    state = []
    for surface_type, asset_ref in sorted(grouped):
        history = grouped[(surface_type, asset_ref)]
        timestamps = [parse_utc(event["observed_at"]) for event in history]
        first_seen = min(timestamps)
        last_seen = max(timestamps)
        duration_days = (last_seen - first_seen).days
        event_count = len(history)
        if duration_days >= 30 or event_count > 10:
            state_level = "persistent"
        elif (7 <= duration_days < 30) or (3 < event_count <= 10):
            state_level = "evolving"
        else:
            state_level = "stable"
        state.append(
            {
                "surface_type": surface_type,
                "asset_ref": asset_ref,
                "first_seen_at": first_seen.isoformat().replace("+00:00", "Z"),
                "last_observed_at": last_seen.isoformat().replace("+00:00", "Z"),
                "event_count_total": event_count,
                "persistence_duration_days": duration_days,
                "last_state_update": recomputed_at,
                "state_level": state_level,
            }
        )
    return state


def validate_events(lines: list[str], events: list[dict], event_schema: dict, rules: dict) -> None:
    seen_ids: set[str] = set()
    history: dict[tuple[str, str], list[dict]] = defaultdict(list)
    previous_time: datetime | None = None
    fingerprint_transition_started = False

    for line_number, (line, event) in enumerate(zip(lines, events, strict=True), start=1):
        validate_instance(event, event_schema, f"journal event line {line_number}")
        if line != canonical_event_line(event):
            raise VerificationError(f"Journal line {line_number} is not canonically serialized")
        if event["event_id"] != canonical_event_id(event):
            raise VerificationError(f"Journal line {line_number} has a non-canonical event_id")
        if event["event_id"] in seen_ids:
            raise VerificationError(f"Journal line {line_number} duplicates an event_id")
        seen_ids.add(event["event_id"])

        surface_type = event["surface_type"]
        rule = rules.get(surface_type)
        if not isinstance(rule, dict):
            raise VerificationError(f"Journal line {line_number} uses an ungoverned surface")
        if not re.fullmatch(rule["asset_ref"]["pattern"], event["asset_ref"]):
            raise VerificationError(f"Journal line {line_number} has an invalid asset_ref")
        source_ref = event["source_ref"]
        parsed = urlparse(source_ref)
        allowed_hosts = rule["source_ref"].get("allowed_hosts", [])
        try:
            explicit_port = parsed.port
        except ValueError as exc:
            raise VerificationError(
                f"Journal line {line_number} has an invalid source_ref port"
            ) from exc
        if (
            parsed.scheme != "https"
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or explicit_port is not None
            or (parsed.hostname or "").lower() not in allowed_hosts
            or source_ref != expected_source_ref(surface_type, event["asset_ref"])
        ):
            raise VerificationError(f"Journal line {line_number} has a non-canonical source_ref")

        observed_at = parse_utc(event["observed_at"])
        if previous_time is not None and observed_at < previous_time:
            raise VerificationError(f"Journal order moves backwards at line {line_number}")
        previous_time = observed_at

        object_key = (surface_type, event["asset_ref"])
        prior_observations = [
            prior for prior in history[object_key] if prior["event_type"] in OBSERVATION_EVENT_TYPES
        ]
        if event["event_type"] in OBSERVATION_EVENT_TYPES:
            if "observable_fingerprint" in event:
                fingerprint_transition_started = True
            elif fingerprint_transition_started:
                raise VerificationError(
                    f"Journal line {line_number} omits observable_fingerprint after its transition"
                )
        if event["event_type"] == "first_seen" and prior_observations:
            raise VerificationError(f"Journal line {line_number} repeats first_seen")
        if event["event_type"] == "reobserved":
            if not prior_observations:
                raise VerificationError(f"Journal line {line_number} reobserves an unseen object")
            interval = observed_at - parse_utc(prior_observations[-1]["observed_at"])
            if interval.total_seconds() < REOBSERVE_INTERVAL_SECONDS:
                raise VerificationError(f"Journal line {line_number} violates the 24h cadence")
        if event["event_type"] in PRIOR_OBSERVATION_REQUIRED_TYPES and not prior_observations:
            raise VerificationError(
                f"Journal line {line_number} records {event['event_type']} before first observation"
            )
        history[object_key].append(event)


def verify_publication(root: Path, public_root: Path, *, full_contract: bool) -> tuple[dict, list[str]]:
    required = (
        "journal/events.jsonl",
        "state/state.json",
        "integrity/publication_manifest.json",
        "integrity/merkle_root.txt",
        "integrity/anchor_payload.json",
        "integrity/proof_status.json",
    )
    for relative in required:
        if not (root / relative).is_file():
            raise VerificationError(f"Missing publication artifact: {root / relative}")

    manifest = load_json(root / "integrity" / "publication_manifest.json")
    anchor_payload = load_json(root / "integrity" / "anchor_payload.json")
    proof_status = load_json(root / "integrity" / "proof_status.json")
    lines, events = read_journal(root)
    journal_path = root / "journal" / "events.jsonl"
    calculated_sha = sha256_file(journal_path)
    calculated_merkle = compute_merkle_root(lines)

    if manifest.get("event_count") != len(lines):
        raise VerificationError(f"event_count mismatch in {root.name}")
    if manifest.get("events_sha256") != calculated_sha:
        raise VerificationError(f"events_sha256 mismatch in {root.name}")
    if manifest.get("merkle_root_sha256") != calculated_merkle:
        raise VerificationError(f"Manifest Merkle root mismatch in {root.name}")
    if (root / "integrity" / "merkle_root.txt").read_text(encoding="utf-8").strip() != calculated_merkle:
        raise VerificationError(f"merkle_root.txt mismatch in {root.name}")
    if anchor_payload.get("publication_id") != manifest.get("publication_id"):
        raise VerificationError(f"Anchor publication mismatch in {root.name}")
    if anchor_payload.get("events_sha256") != calculated_sha:
        raise VerificationError(f"Anchor journal digest mismatch in {root.name}")
    if anchor_payload.get("merkle_root_sha256") != calculated_merkle:
        raise VerificationError(f"Anchor Merkle root mismatch in {root.name}")
    if anchor_payload.get("journal_path") != "journal/events.jsonl":
        raise VerificationError(f"Anchor journal path mismatch in {root.name}")
    if proof_status.get("publication_id") != manifest.get("publication_id"):
        raise VerificationError(f"Proof status publication mismatch in {root.name}")

    anchor_path = root / "integrity" / "anchor.ots"
    snapshot_status = proof_status.get("status")
    if snapshot_status == "pending_ots" and anchor_path.exists():
        raise VerificationError(f"pending_ots snapshot contains anchor.ots: {root.name}")
    if snapshot_status != "pending_ots" and (not anchor_path.exists() or anchor_path.stat().st_size <= 0):
        raise VerificationError(f"Non-pending snapshot lacks anchor.ots: {root.name}")

    if full_contract:
        schema_names = (
            "event.schema.json",
            "publication_manifest.schema.json",
            "proof_status.schema.json",
            "proof_attestation.schema.json",
            "state.schema.json",
        )
        schemas = {
            name: validate_schema(root / "schemas" / name)
            for name in schema_names
        }
        validate_instance(manifest, schemas["publication_manifest.schema.json"], "manifest")
        validate_instance(proof_status, schemas["proof_status.schema.json"], "proof status")
        taxonomy = load_json(root / "taxonomy" / "surface_rules.json")
        rules = taxonomy.get("surface_rules")
        if not isinstance(rules, dict):
            raise VerificationError(f"Invalid published surface rules in {root.name}")
        validate_events(lines, events, schemas["event.schema.json"], rules)
        state = load_json(root / "state" / "state.json")
        validate_instance(state, schemas["state.schema.json"], "derived state")
        if state != replay_state(events, manifest["published_at"]):
            raise VerificationError(f"Derived state replay mismatch in {root.name}")
        if anchor_payload.get("contract_profile") != HARDENED_CONTRACT_PROFILE:
            raise VerificationError(f"Anchor payload lacks the hardened profile in {root.name}")

    return manifest, lines


def canonical_snapshot_dirs(public_root: Path) -> list[Path]:
    snapshots_root = public_root / "snapshots"
    if not snapshots_root.is_dir():
        raise VerificationError(f"Missing snapshots directory: {snapshots_root}")
    unexpected = [
        child.name
        for child in snapshots_root.iterdir()
        if not child.is_dir() or not SNAPSHOT_RE.fullmatch(child.name)
    ]
    if unexpected:
        raise VerificationError(f"Unexpected entries in snapshots/: {sorted(unexpected)}")
    return sorted(snapshots_root.iterdir())


def verify_immutability_ledger(public_root: Path, snapshots: list[Path]) -> dict:
    ledger = load_json(public_root / "immutability_ledger.json")
    if ledger.get("contract_profile") != HARDENED_CONTRACT_PROFILE:
        raise VerificationError("Invalid immutability ledger contract profile")
    entries = ledger.get("snapshots")
    if not isinstance(entries, dict):
        raise VerificationError("Immutability ledger snapshots must be an object")
    snapshot_names = {snapshot.name for snapshot in snapshots}
    if set(entries) != snapshot_names:
        raise VerificationError("Immutability ledger coverage does not match snapshots/")
    for snapshot in snapshots:
        entry = entries[snapshot.name]
        if not isinstance(entry, dict):
            raise VerificationError(f"Invalid ledger entry: {snapshot.name}")
        if entry.get("tree_sha256") != directory_tree_digest(snapshot):
            raise VerificationError(f"Immutable snapshot digest mismatch: {snapshot.name}")
    return ledger


def verify_attestations(public_root: Path, snapshots: dict[str, Path], schema: dict) -> int:
    attestations_root = public_root / "attestations"
    if not attestations_root.exists():
        return 0
    if not attestations_root.is_dir():
        raise VerificationError("attestations must be a directory")
    count = 0
    for publication_root in sorted(attestations_root.iterdir()):
        publication_id = publication_root.name
        if not publication_root.is_dir() or publication_id not in snapshots:
            raise VerificationError(f"Invalid attestation publication directory: {publication_id}")
        revision_roots = sorted(
            child for child in publication_root.iterdir() if child.is_dir() and REVISION_RE.fullmatch(child.name)
        )
        extras = [
            child.name
            for child in publication_root.iterdir()
            if not (child.name == "latest.json" or (child.is_dir() and REVISION_RE.fullmatch(child.name)))
        ]
        if extras or not revision_roots:
            raise VerificationError(f"Invalid attestation layout for {publication_id}")
        snapshot_manifest = load_json(
            snapshots[publication_id] / "integrity" / "publication_manifest.json"
        )
        previous_manifest_sha = None
        for index, revision_root in enumerate(revision_roots, start=1):
            if revision_root.name != f"r{index:06d}":
                raise VerificationError(f"Attestation revision gap for {publication_id}")
            files = {child.name for child in revision_root.iterdir() if child.is_file()}
            if files != {"anchor.ots", "attestation_manifest.json"}:
                raise VerificationError(f"Invalid attestation revision layout: {revision_root}")
            manifest_path = revision_root / "attestation_manifest.json"
            anchor_path = revision_root / "anchor.ots"
            manifest = load_json(manifest_path)
            validate_instance(manifest, schema, f"attestation {publication_id}/{revision_root.name}")
            if manifest.get("publication_id") != publication_id:
                raise VerificationError(f"Attestation publication mismatch: {revision_root}")
            if manifest.get("revision_id") != revision_root.name:
                raise VerificationError(f"Attestation revision mismatch: {revision_root}")
            if manifest.get("snapshot_merkle_root_sha256") != snapshot_manifest.get("merkle_root_sha256"):
                raise VerificationError(f"Attestation Merkle root mismatch: {revision_root}")
            if manifest.get("snapshot_events_sha256") != snapshot_manifest.get("events_sha256"):
                raise VerificationError(f"Attestation journal digest mismatch: {revision_root}")
            if (
                not anchor_path.is_file()
                or anchor_path.stat().st_size <= 0
                or manifest.get("anchor_ots_sha256") != sha256_file(anchor_path)
            ):
                raise VerificationError(f"Attestation OTS digest mismatch: {revision_root}")
            if manifest.get("previous_revision_manifest_sha256") != previous_manifest_sha:
                raise VerificationError(f"Attestation hash-chain mismatch: {revision_root}")
            previous_manifest_sha = sha256_file(manifest_path)
            count += 1

        pointer = load_json(publication_root / "latest.json")
        latest_root = revision_roots[-1]
        if pointer.get("publication_id") != publication_id or pointer.get("revision_id") != latest_root.name:
            raise VerificationError(f"Attestation latest pointer mismatch: {publication_id}")
        if pointer.get("manifest_path") != f"{latest_root.name}/attestation_manifest.json":
            raise VerificationError(f"Attestation latest path mismatch: {publication_id}")
        if pointer.get("manifest_sha256") != sha256_file(latest_root / "attestation_manifest.json"):
            raise VerificationError(f"Attestation latest digest mismatch: {publication_id}")
    return count


def verify_public_root(public_root: Path) -> dict:
    public_root = public_root.resolve()
    snapshots = canonical_snapshot_dirs(public_root)
    ledger = verify_immutability_ledger(public_root, snapshots)
    previous_lines: list[str] | None = None
    previous_published_at: datetime | None = None
    hardened_count = 0
    manifests: dict[str, dict] = {}

    for snapshot in snapshots:
        manifest_hint = load_json(snapshot / "integrity" / "publication_manifest.json")
        full_contract = manifest_hint.get("contract_profile") == HARDENED_CONTRACT_PROFILE
        manifest, lines = verify_publication(
            snapshot,
            public_root,
            full_contract=full_contract,
        )
        if manifest.get("publication_id") != snapshot.name:
            raise VerificationError(f"Snapshot identity mismatch: {snapshot.name}")
        if previous_lines is not None and lines[: len(previous_lines)] != previous_lines:
            raise VerificationError(f"Journal is not a prefix extension at {snapshot.name}")
        published_at = parse_utc(manifest["published_at"])
        if previous_published_at is not None and published_at < previous_published_at:
            raise VerificationError(f"Publication time moved backwards at {snapshot.name}")
        previous_lines = lines
        previous_published_at = published_at
        manifests[snapshot.name] = manifest
        if full_contract:
            hardened_count += 1

    if not snapshots or hardened_count == 0:
        raise VerificationError("No hardened canonical snapshot is published")
    current = public_root / "current"
    current_manifest = load_json(current / "integrity" / "publication_manifest.json")
    latest_snapshot = snapshots[-1]
    if current_manifest.get("publication_id") != latest_snapshot.name:
        raise VerificationError("current/ does not reference the latest canonical snapshot")
    if directory_tree_digest(current) != directory_tree_digest(latest_snapshot):
        raise VerificationError("current/ is not byte-identical to its canonical snapshot")
    verify_publication(current, public_root, full_contract=True)

    attestation_schema = validate_schema(current / "schemas" / "proof_attestation.schema.json")
    attestation_count = verify_attestations(
        public_root,
        {snapshot.name: snapshot for snapshot in snapshots},
        attestation_schema,
    )
    return {
        "publication_id": latest_snapshot.name,
        "event_count": current_manifest["event_count"],
        "snapshot_count": len(snapshots),
        "hardened_snapshot_count": hardened_count,
        "ledger_entry_count": len(ledger["snapshots"]),
        "attestation_revision_count": attestation_count,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the complete RegistryOps public contract without privileged repository access."
    )
    parser.add_argument("--public-root", default=".")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = verify_public_root(Path(args.public_root))
    except VerificationError as exc:
        print(f"REGISTRYOPS PUBLIC VERIFICATION FAILED: {exc}")
        raise SystemExit(1) from exc
    print(
        "REGISTRYOPS PUBLIC VERIFICATION PASSED "
        f"(publication={result['publication_id']}, events={result['event_count']}, "
        f"snapshots={result['snapshot_count']}, hardened={result['hardened_snapshot_count']}, "
        f"attestations={result['attestation_revision_count']})"
    )


if __name__ == "__main__":
    main()
