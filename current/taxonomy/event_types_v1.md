# event_types_v1

## Purpose
Define the closed list of factual event types observable across eligible surfaces.
Event types are descriptive and non-evaluative.

---

## event_type v1 (closed list)

### surface_presence_observed
A surface is observed to exist and be publicly accessible.

### surface_absence_observed
A surface previously observed is no longer publicly accessible.

### artifact_version_published
A new public artifact or version is published.

### artifact_version_removed
A previously published public artifact or version is no longer available.

### metadata_changed
A change is observed in globally published metadata.

### availability_state_changed
A global availability state transitions (e.g. unavailable → available).

### verification_status_changed
A public verification or attestation status changes.

### specification_status_changed
A public specification or standard status changes.

---

## event_type to surface_type mapping

- surface_presence_observed  
  Applies to: all surface_type

- surface_absence_observed  
  Applies to: all surface_type

- artifact_version_published  
  Applies to: software_package, standard_spec, governance_doc

- artifact_version_removed  
  Applies to: software_package, standard_spec, governance_doc

- metadata_changed  
  Applies to: all surface_type

- availability_state_changed  
  Applies to: public_api, service_status_page, data_feed_public

- verification_status_changed  
  Applies to: smart_contract

- specification_status_changed  
  Applies to: standard_spec, governance_doc
