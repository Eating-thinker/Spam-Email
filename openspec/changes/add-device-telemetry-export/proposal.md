## Why

Instructors and students need an easy way to export collected device telemetry for offline analysis, grading, or visualization. Currently telemetry is stored locally but there is no standardized, exportable format or API to retrieve filtered data sets.

## What Changes

- Add a telemetry export capability that exposes an authenticated API endpoint to request telemetry exports for a specified device/time-range in CSV format.
- Add a CLI utility to generate CSV exports from the local store.
- Add spec deltas for the `telemetry` capability (ADDED Requirements).

**BREAKING**: none.

## Impact

- Affected specs: `telemetry` (new ADDED requirement)
- Affected code: `services/telemetry_ingest`, `services/api` (new endpoint), `tools/telemetry_export.py` (new CLI)
- Affected infra: local MQTT broker and storage access. No cloud infra required.

## Rollout Plan

1. Add proposal and spec deltas (this change).
2. Implement the API endpoint and CLI, plus unit/integration tests.
3. Validate with `openspec validate add-device-telemetry-export --strict` and run CI.
4. Request review and approval via PR. Merge once approved.

## Migration

No migration needed. Existing telemetry storage remains backward-compatible. Export is additive.

## Risks and Mitigations

- Risk: Export may expose sensitive data. Mitigation: enforce that exports only include non-PII fields and require authenticated access.
- Risk: Large exports may consume memory. Mitigation: stream CSV generation from the DB instead of loading all rows.

## Open Questions

- Which fields should be included in CSV exports by default? (recommended: timestamp, device_id, sensor readings flattened)
- Preferred authentication mechanism for the export endpoint? (token-based assumed)

## Acceptance Criteria

- Proposal and spec delta exist under `openspec/changes/add-device-telemetry-export/`.
- API endpoint documented and implemented in tasks.md.
- At least one unit test and one integration smoke test for export functionality.
