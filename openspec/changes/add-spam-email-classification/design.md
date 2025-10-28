## Context

We will build a small, reproducible ML pipeline for spam classification targeting classroom use. Keep dependencies minimal and results easy to interpret.

## Dataset

- Source: `sms_spam_no_header.csv` from the provided repository. The CSV typically contains two columns: label (spam/ham) and text.

## Preprocessing

- Text cleaning: lowercasing, remove punctuation, basic tokenization.
- Feature extraction: TF-IDF vectorizer over tokens (limit vocabulary size to keep memory low).
- Use stratified train/test split (e.g., 80/20) and set a fixed random seed for reproducibility.

## Models

- Primary: Logistic Regression (scikit-learn). Advantages: fast, interpretable coefficients.
- Comparator: SVM (scikit-learn) — optional baseline comparison to show difference in behavior.

## Evaluation

- Report precision, recall, F1-score, accuracy, and confusion matrix.
- Export model artifact and an evaluation report (JSON or simple text).

## Reproducibility

- Fix random seeds where applicable and log package versions in `ml/requirements.txt` and `ml/README.md`.

## Resource Constraints

- Keep memory usage low by limiting TF-IDF vocabulary and using scikit-learn's efficient implementations.
