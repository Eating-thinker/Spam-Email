## Why

We want a reproducible, documented project to build and evaluate a spam email classifier using classical machine learning. This will serve as a learning exercise in preprocessing, model selection, evaluation, and minimal deployment/export of results for grading and demonstration.

## Goal

Build a spam email classification pipeline using logistic regression as the primary model. Provide a clear baseline (Phase 1) and placeholders for follow-on phases.

## What Changes

- Add a new ML capability `spam-classification` with an initial baseline implementation (Phase 1).
- Provide training scripts, evaluation artifacts (metrics and model artifact), and a small CLI to reproduce training and export results.
- Use the public dataset linked below as the training corpus.

Data source (public):
- https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/blob/master/Chapter03/datasets/sms_spam_no_header.csv

## Phases

- Phase 1 - Baseline: Implement data ingestion and a baseline classifier (logistic regression). Optionally train an SVM in the baseline to compare results.
- Phase 2 - (reserved)
- Phase 3 - (reserved)
- Phase N - (reserved)

## Impact

- Affected specs: `ml/spam-classification` (new capability)
- Affected code: `ml/` (new module), `tools/` (reproducible CLI), and optional `services/api` if model serving is later added.
- Affected infra: none required beyond local compute and Python dependencies.

## Rollout Plan

1. Create proposal (this file) and spec delta under `openspec/changes/add-spam-email-classification/specs/`.
2. Implement Phase 1: data download, preprocessing, training script, evaluation, and CLI for reproducible runs.
3. Add unit tests and a small integration test that trains on a tiny sample and verifies output artifacts.
4. Validate with `openspec validate add-spam-email-classification --strict`, open PR, request review.

## Migration

This is an additive change. No migration steps required.

## Risks and Mitigations

- Risk: Dataset licensing or availability. Mitigation: include a local copy under `data/` with provenance notes or fall back to a mirrored dataset.
- Risk: Unbalanced classes may yield misleading accuracy. Mitigation: report precision/recall/F1 and use stratified splits.

## Open Questions

- Confirm model choice: you mentioned logistic regression and SVM; do you want logistic regression as primary and SVM as an optional comparator in Phase 1?
- Any constraints on runtime or resource usage (e.g., must run within 2 minutes on a standard laptop)?

## Acceptance Criteria

- `openspec/changes/add-spam-email-classification/` exists with `proposal.md`, `tasks.md`, and spec delta(s).
- A runnable script `ml/train_baseline.py` (or similar) trains a logistic regression model on the provided dataset and writes a model artifact and evaluation report.
- A CLI `tools/train_spam_baseline.py` reproduces the baseline run.
