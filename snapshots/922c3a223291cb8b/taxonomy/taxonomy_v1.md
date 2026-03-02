# Taxonomy v1 — Surfaces and Event Types

## 1. Scope
This taxonomy defines the initial, minimal, and canonical set of:
- observation surface types,
- event types
allowed in the public temporal registry.

Only the terms defined in this document are permitted in registry events.

## 2. Surface Types

Surface types describe the category of public surface on which an event is observed.
They are abstract, non-personal, and technology-oriented.

### 2.1 Allowed Surface Types

- `public_code_repository`  
  Public source code repositories accessible without authentication.

- `package_registry`  
  Public software package registries.

- `domain_name_system`  
  Public DNS-related records and metadata.

- `certificate_transparency_log`  
  Public certificate transparency and issuance logs.

- `open_government_dataset`  
  Institutional or governmental open data catalogs.

- `public_technical_registry`  
  Any other public technical registry not covered above.

### 2.2 Forbidden Surface Types

The following are explicitly forbidden:
- social networks or social platforms,
- user accounts or profiles,
- forums, comments, or user-generated discussions,
- any surface requiring authentication or access circumvention.

## 3. Event Types

Event types describe neutral, observable facts related to an asset.

### 3.1 Allowed Event Types

- `first_observed`  
  The asset is observed for the first time on a given surface.

- `observed`  
  The asset is observed at a given point in time without implying change.

- `updated`  
  A non-semantic change to the asset is observed.

- `removed`  
  The asset is no longer observed on the surface.

- `policy_changed`  
  A public policy or configuration related to the asset has changed.

### 3.2 Forbidden Event Types

The following are not allowed:
- any event implying wrongdoing, intent, or evaluation,
- security incidents, abuse, fraud, or reputation-related events,
- events describing individuals or personal actions.

## 4. Extension Rules
- New surface types or event types must be:
  - neutral and factual,
  - non-personal by design,
  - observable on public surfaces without authentication.
- Any extension must be versioned and backward-compatible.
