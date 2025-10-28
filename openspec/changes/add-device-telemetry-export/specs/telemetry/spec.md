## ADDED Requirements

### Requirement: Telemetry export API
The system SHALL provide an HTTP API to export collected telemetry for a given device and time range in CSV format.

#### Scenario: Successful CSV export via API
- **WHEN** a client requests `GET /exports/telemetry?device_id=dev-123&from=2025-10-01T00:00:00Z&to=2025-10-01T01:00:00Z&format=csv` with valid credentials
- **THEN** the server SHALL respond with `200 OK` and `Content-Type: text/csv` and stream CSV rows covering the specified time range

#### Scenario: Unauthorized request is rejected
- **WHEN** a client requests the export endpoint without valid credentials
- **THEN** the server SHALL respond with `401 Unauthorized`

### Requirement: Telemetry export CLI
The system SHALL provide a CLI utility that produces the same CSV output as the API for offline/export use.

#### Scenario: CLI exports CSV to file
- **WHEN** a user runs `tools/telemetry_export.py --device dev-123 --from 2025-10-01T00:00:00Z --to 2025-10-01T01:00:00Z --out sample.csv`
- **THEN** the CLI SHALL create `sample.csv` containing the telemetry rows in the same column order and format as the API export
