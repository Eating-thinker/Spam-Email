## Context

Exporting telemetry should be efficient and safe. Data should be streamed from storage to avoid large memory use. Exports must avoid including any PII.

## Goals / Non-Goals
- Goals: provide a filtered, streamable CSV export endpoint and CLI; keep implementation simple and testable.
- Non-Goals: build a full analytics pipeline or long-term archival storage.

## Decisions

- API: add `GET /exports/telemetry` with query params `device_id`, `from`, `to`, `format` (csv). The API will stream with `text/csv` and use per-request authentication token.
- CLI: simple script using the same export codepath to avoid duplication.
- DB access: query with a cursor/iterator, stream row-by-row.

## Data Model (minimal)

Telemetry table (example):
- id (PK)
- device_id (string)
- ts (ISO-8601 timestamp)
- payload (JSON blob) — for CSV we will flatten top-level numeric sensor fields into columns

## Migration Plan

- None required.

## Risks
- Large time ranges: stream and limit default to 24h unless user specifies otherwise.

## Open Questions
- CSV column ordering and handling nested JSON in `payload` (flattening rules). Default: include timestamp, device_id, and a JSON-encoded `payload` column if flattening is not possible.
