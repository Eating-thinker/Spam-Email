# Project Context

## Purpose
This repository contains an IoT homework project focused on device telemetry collection, processing, and simple visualization for learning and experimentation. The primary goal is to provide a reproducible, well-documented codebase for collecting device data (telemetry), running small-scale processing/validation, and exporting or visualizing results for instructors and students.

## Tech Stack
- [List your primary technologies]
- [e.g., TypeScript, React, Node.js]
Primary technologies and tools used in this project (assumptions noted below):

- Python 3.10+ (core services and scripts)
- FastAPI (lightweight HTTP APIs)
- paho-mqtt (MQTT client for device telemetry)
- SQLite (local persistence for homework) — may be swapped for Postgres in larger deployments
- React (optional frontend/dashboard)
- GitHub Actions (CI for tests and linting)

Assumptions: This repo targets an educational IoT stack; if your project uses different languages/frameworks (e.g., Node.js, MicroPython, or platform-specific SDKs), update this section accordingly.

## Project Conventions

### Code Style
[Describe your code style preferences, formatting rules, and naming conventions]
Code style and formatting
- Python: follow PEP 8; use black for formatting and isort for imports
- JavaScript/TypeScript (if present): follow ESLint + Prettier defaults
- Use descriptive, lower_snake_case (Python) or lowerCamelCase (JS) for identifiers.
- Write concise docstrings for public functions and modules. Include type hints in Python.

### Architecture Patterns
[Document your architectural decisions and patterns]
Architecture patterns
- Simple service-per-responsibility: a telemetry-ingest service (MQTT subscriber) and a small API service (FastAPI) for querying/exporting data. Frontend is a separate SPA that calls the API.
- Keep data models shallow and explicit for teaching clarity.
- Prefer synchronous request/response for API; use background workers for heavy processing.

### Testing Strategy
[Explain your testing approach and requirements]
Testing
- Unit tests with pytest for Python code. Aim for small, fast tests.
- Integration tests for core flows: ingest -> store -> export.
- Minimal end-to-end smoke test that starts services (or uses fixtures/mocks) to validate telemetry pipeline.
- CI runs linting and tests on PRs.

### Git Workflow
[Describe your branching strategy and commit conventions]
Git & branching
- Main branch: `main` (always deployable / instructor-verified state)
- Development: create short-lived feature branches named `feat/<short-desc>` or `fix/<short-desc>`.
- Commit messages: use imperative tense, short subject line, and optional body. Example: `feat: add telemetry CSV export`
- Pull requests: include link to the relevant OpenSpec change under `openspec/changes/` when applicable.

## Domain Context
[Add domain-specific knowledge that AI assistants need to understand]
Domain context
- Devices publish telemetry over MQTT to a broker (topic per-device or per-type).
- Telemetry payloads are JSON objects containing timestamp, device_id, and sensor readings.
- Typical payload size is small (<2 KB) and messages are frequent (per-second to per-minute depending on scenario).

## Important Constraints
[List any technical, business, or regulatory constraints]
Important constraints
- Keep resource usage low — intended for local or classroom environments.
- No PII collection in telemetry samples used for coursework.
- Solutions should be easy to run locally (no heavy infra required).

## External Dependencies
[Document key external services, APIs, or systems]
External dependencies
- MQTT broker (Mosquitto recommended for local testing)
- Optional: external telemetry sinks (CSV export, S3, or third-party analytics). Document credentials separately and do not commit secrets.

Contacts
- Maintainer: <your-name-or-email>
- Course instructor: <instructor-email>

Notes / Next steps
- If any of the assumptions above are incorrect (language/runtime, DB choice, or frontend stack), tell me which stack to use and I will adapt files and the proposal accordingly.
