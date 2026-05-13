# RegistryOps Normative Hierarchy

RegistryOps phase 1 defines an explicit hierarchy between doctrine, executable
norms, implementation, and public publication.

The phase 1.1 observable-fingerprint extension and the phase 1.2 external
proof-closure extension follow the same hierarchy and do not create separate
normative lines.

## Priority Order

In case of conflict, the following order prevails:

1. `ops/` constitutional corpus
2. `registry/spec/` and `registry/taxonomy/` executable normative corpus
3. `registry/scripts/` reference implementation
4. `docs/` explanatory documentation
5. `registry/public/` derived public publication

## Interpretation Rule

The codebase does not define the sovereign rule by itself.

The implementation must conform to the constitutional corpus and to the
executable normative corpus. Public artifacts are derived outputs and therefore
cannot override the rule that governs them.

## Phase 1 Mapping

- `ops/` defines the constitutional rule of RegistryOps phase 1.
- `registry/spec/` and `registry/taxonomy/` express the executable public rule,
  including the phase 1.1 observable-fingerprint extension and the phase 1.2
  proof-closure extension.
- `registry/scripts/` implement the reference behavior of ingestion,
  validation, publication, and proof.
- `docs/` explain the system but do not have normative authority.
- `registry/public/` exposes the official public contract once built.
