# RegistryOps Event Types

This document defines the closed set of authorized `event_type` values for RegistryOps.

This document is subordinate to **RegistryOps Canonical Specification**.

In case of divergence, **RegistryOps Canonical Specification** prevails.

## Scope

RegistryOps authorizes only a minimal closed vocabulary of event types.

The purpose of this vocabulary is to preserve semantic stability, minimize interpretive drift, and ensure that all observers emit events within a strictly controlled grammar.

No `event_type` outside this document is allowed in RegistryOps.

## Authorized `event_type` Values

RegistryOps authorizes only the following values:

- `first_seen`
- `state_changed`
- `withdrawn`
- `revoked`
- `replaced`
- `expired`
- `unreachable`

No other `event_type` value is allowed in RegistryOps.

## Normative Semantics

### `first_seen`

Issued when an asset or observable state is publicly seen for the first time by RegistryOps.

This event type is used only for the first public observation recorded by RegistryOps for the relevant observable object or state.

### `state_changed`

Issued when a previously known observable state presents a publicly verifiable modification that does not fall under a more specific event type.

`state_changed` is a residual event type and must not be used when a more specific authorized event type applies.

### `withdrawn`

Issued when a previously observable state or object has been removed from the relevant public surface.

This event type applies when public availability or public presence has been withdrawn, without implying revocation, replacement, or expiration unless such status is explicitly observable.

### `revoked`

Issued when an observed object becomes subject to an explicit public revocation.

This event type must be used only when revocation is itself publicly observable and not merely inferred.

### `replaced`

Issued when an observable state is explicitly replaced by another state on the same surface.

This event type applies when replacement is the relevant observable fact, rather than a generic modification.

### `expired`

Issued when an observable state publicly reaches the end of its validity or expiration.

This event type must be used only when expiration is itself publicly observable.

### `unreachable`

Issued when an expected public surface or source becomes unreachable at observation time, without by itself implying withdrawal, revocation, replacement, or expiration.

`unreachable` records an observation failure condition on a public surface, not a semantic conclusion about the asset itself.

## Interpretation Rule

When a single observation could plausibly match multiple authorized event types, the implementation must select the most specific applicable event type.

`state_changed` must be used only when no more specific authorized event type applies.

## Closed Vocabulary Rule

The `event_type` vocabulary of RegistryOps is closed.

The following categories of values are not allowed in the canonical taxonomy:

- legacy event names
- observer-specific event names
- compatibility aliases
- inferred semantic extensions
- surface-local custom event types

Any extension of the `event_type` vocabulary requires an explicit revision of the canonical specification and therefore belongs to a future version, not to the current canonical taxonomy.

## Compliance Rule

An implementation is compliant with RegistryOps only if it emits events using exclusively the seven authorized `event_type` values defined in this document and in the canonical specification.