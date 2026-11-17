# RegistryOps Normative Hierarchy

RegistryOps defines an explicit hierarchy between doctrine, executable norms,
implementation, and public publication.

The phase 1.1 observable-fingerprint extension, the phase 1.2 external
proof-closure extension, and the phase 2 surface-expansion rule follow the same
hierarchy.

For publications declaring `registryops-contract-2026-07`, conflicts inside
the constitutional corpus are resolved by
`ops/contract_hardening_transition_2026_07.md`, which explicitly identifies the
legacy rule being superseded and preserves the historical record unchanged.

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

## Mapping

- `ops/` defines the constitutional rule of RegistryOps.
- `registry/spec/` and `registry/taxonomy/` express the executable public rule,
  including active surfaces and proof extensions.
- `registry/scripts/` implement the reference behavior of ingestion,
  validation, publication, and proof.
- `docs/` explain the system but do not have normative authority.
- `registry/public/` exposes the official public contract once built.
