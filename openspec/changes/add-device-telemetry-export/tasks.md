## 1. Implementation
- [ ] 1.1 Create API endpoint: `GET /exports/telemetry?device_id=<id>&from=<ts>&to=<ts>&format=csv`
- [ ] 1.2 Implement streaming CSV generator that queries the DB and streams results
- [ ] 1.3 Add authentication/authorization guard for the endpoint
- [ ] 1.4 Add CLI tool `tools/telemetry_export.py --device <id> --from <ts> --to <ts> --out file.csv`
- [ ] 1.5 Add unit tests for CSV generator and endpoint handlers
- [ ] 1.6 Add integration test: ingest sample telemetry and request export

## 2. Docs
- [ ] 2.1 Document the endpoint in the API README
- [ ] 2.2 Add usage examples for the CLI

## 3. Validation
- [ ] 3.1 Run `openspec validate add-device-telemetry-export --strict`
- [ ] 3.2 Ensure CI passes (lint + tests)
