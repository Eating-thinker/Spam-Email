## ADDED Requirements

### Requirement: Spam email classification baseline
The system SHALL provide a reproducible baseline pipeline that trains and evaluates a spam email classifier using logistic regression on the provided dataset.

#### Scenario: Train and evaluate baseline model
- **WHEN** a developer runs the baseline training script with the dataset present
- **THEN** the system SHALL produce a model artifact and an evaluation report containing precision, recall, F1, accuracy, and a confusion matrix

#### Scenario: CLI reproduction
- **WHEN** a user runs the CLI `tools/train_spam_baseline.py --data data/sms_spam_no_header.csv --out ml/results/` with valid inputs
- **THEN** the CLI SHALL produce the same model artifact and evaluation report as the programmatic training script, assuming fixed random seeds
