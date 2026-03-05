# surfaces_v1

## Purpose
Define the types of public, observable surfaces eligible for inclusion in the registry.
This list is closed and versioned for v1.

---

## surface_type v1 (closed list)

### 1. code_repository
Public source code repository accessible without authentication.
Excludes any contributor, author, or account-level information.

### 2. software_package
Software package published in a public registry.
Includes only global package metadata.

### 3. domain_name
Public DNS domain name.
Explicitly excludes WHOIS data or ownership information.

### 4. smart_contract
Contract deployed on a public blockchain.
Observation limited to existence and global metadata.

### 5. blockchain_network
Identifiable public blockchain network.
Includes only network-wide parameters.

### 6. public_api
Publicly documented API.
Observation limited to availability and published version.

### 7. data_feed_public
Publicly accessible data feed without access restrictions.
Excludes any individualized or user-level data.

### 8. service_status_page
Official public service status page.
Includes only global service states.

### 9. standard_spec
Publicly published standard or specification (e.g. RFC).
Observation limited to official versions and status.

### 10. governance_doc
Public, non-personalized governance document.
Includes only version or status changes.

---

## Surface eligibility rules

A surface is eligible for inclusion in the registry if and only if ALL of the following conditions are met:

1. Public accessibility  
   The surface MUST be accessible without authentication, login, or user-specific access.

2. Non-personal nature  
   The surface MUST NOT represent, reference, or depend on a natural person, user account, or individual activity.

3. Stability over time  
   The surface MUST have a stable identifier or reference that persists over time.

4. Passive observability  
   The surface MUST be observable in read-only mode without interaction or behavioral tracking.

5. Intermediate granularity  
   The surface MUST expose global or aggregated state, not fine-grained user-level events.

---

## Explicit exclusions

The following are explicitly excluded from eligibility:

- User profiles or personal pages
- Accounts, handles, or identifiers tied to individuals
- Comment threads, discussions, or social interactions
- Activity logs linked to specific actors
- Any surface requiring authentication or personalized access

---

## source_ref v1 (generic sources)

The source_ref field indicates the generic origin of an observation.
It MUST NOT identify a specific observer, account, or access path.

### Allowed source_ref values

- public_web_snapshot  
  Observation derived from a public web-accessible surface.

- official_status_page  
  Observation derived from an official public status or uptime page.

- public_registry_index  
  Observation derived from a public package, domain, or artifact index.

- blockchain_node_public  
  Observation derived from a publicly accessible blockchain node.

- open_metadata_feed  
  Observation derived from an openly accessible metadata feed.

- official_documentation  
  Observation derived from publicly published official documentation.

### Optional hashing

A non-reversible hash MAY be used to reference the exact access path internally.
This hash MUST NOT be required and MUST NOT be reversible or human-readable.

---

## source_ref prohibitions

The following are strictly prohibited in source_ref:

- Full URLs or URL fragments
- Query parameters or request paths
- Account names, handles, or identifiers
- Email addresses or contact information
- API keys, tokens, or credentials

---

## Observation rules

Observation rules define what kinds of signals are allowed to generate events in the registry.

### Allowed observations

The following observation types are permitted:

- Existence or non-existence of a surface
- Publication or removal of a public artifact
- Version changes of public artifacts or specifications
- Binary availability states (available / unavailable)
- Changes in globally published metadata
- Network- or system-wide state changes

All allowed observations MUST:
- Be derived from public, non-authenticated access
- Reflect global or aggregated state only
- Be reproducible by any third party

### Forbidden observations

The following observation types are strictly forbidden:

- User-initiated actions or behaviors
- Activity attributable to specific individuals or accounts
- Comment content, discussions, or social interactions
- Access logs, usage analytics, or traffic metrics
- Fine-grained temporal tracking of human actions
- Any form of behavioral profiling

Any observation requiring interaction, authentication, or inference about individual actors is prohibited.

---

## Examples

### Conform examples

The following examples are compliant with all surface and observation rules:

- surface_type: software_package  
  Observation: a new package version is published in a public registry  
  Event type: package_version_published

- surface_type: smart_contract  
  Observation: a contract becomes publicly verified on a blockchain explorer  
  Event type: contract_verified_publicly

- surface_type: domain_name  
  Observation: a domain transitions from inactive to active DNS resolution  
  Event type: domain_activation_observed

- surface_type: service_status_page  
  Observation: a global service status changes from degraded to operational  
  Event type: service_status_changed

### Non-conform examples

The following examples are explicitly non-compliant and prohibited:

- Observing commit activity by a specific author in a code repository
- Tracking publication times correlated to a specific maintainer
- Monitoring user comments, issues, or discussion threads
- Recording access frequency or traffic patterns of a public API
- Inferring human behavior or intent from temporal activity patterns
