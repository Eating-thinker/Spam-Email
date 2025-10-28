# Spam Email Classification

This project implements a reproducible spam (SMS/email) classification pipeline with a baseline and a stronger tuned pipeline, plus a Streamlit demo app to try predictions locally.

Contents
- `ml/` — training code and utilities
  - `train_baseline.py` — quick baseline (TF-IDF + LogisticRegression)
  - `train_strong.py` — stronger pipeline with GridSearchCV across TF-IDF and classifiers
  - `preprocess.py` — CSV loader and helpers
- `tools/` — CLI wrappers
- `demo/streamlit_app.py` — Streamlit demo for single and batch predictions
- `data/` — included sample CSV for quick smoke testing
- `ml/results/` — default output location for models and reports

Quick start

1. Install Python 3.10+ and create a venv (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r ml/requirements.txt
```

2. Run the baseline (fast):

```powershell
python tools/train_spam_baseline.py --data data/sample_sms.csv --out ml/results_sample
```

3. Run the stronger training (GridSearch — may take longer):

```powershell
python ml/train_strong.py --data data/sample_sms.csv --out ml/results_sample_strong --jobs 2
```

4. Run the Streamlit demo locally:

```powershell
streamlit run demo/streamlit_app.py
```

Reproducing with the public dataset
- Download or point `--data` to the dataset CSV (for example the PacktPublishing dataset), and run the training scripts as above.

Model artifact
- Models and reports are saved under the `--out` directory. The stronger training saves `spam_best_model.joblib` and `report.json`.

Notes
- For classroom use: avoid using real PII in datasets. This project uses small sample data for illustrative purposes.

Live demo

We host a live demo of this app on Streamlit Cloud:

- https://spam-email-6jmdv6han65mi36einbpuj.streamlit.app/

Live demo details and usage

- What the demo shows:
  - Single-text prediction: paste an email or SMS text and click Predict to get a SPAM/HAM classification and probabilities (if available).
  - Dataset viewer & training stats: upload a CSV (no header; columns: `label,text`) or use the included sample. The app shows a preview, class distribution, message length histogram, top tokens, and example messages by class.
  - Batch prediction: upload a CSV of examples and the app will generate predictions and write them to `.tmp/predictions.jsonl` in the app environment (downloadable when run locally).

- Example quick workflow on the live demo:
  1. Open the live demo link above.
  2. Paste a message into the Single-text input and click Predict.
  3. (Optional) Upload your dataset CSV to inspect class balance and top tokens.
  4. Train a model locally using `ml/train_strong.py` and then upload the resulting joblib model to the demo to test it live.

- Security & privacy notes:
  - Do not upload PII or sensitive data to the public demo. For private model evaluation use the app locally.
  - Models saved in Git should avoid embedding secrets or user data. Consider hosting model artifacts externally for larger models.

- Troubleshooting (common issues):
  - "No model available" on the demo: train a model locally (see Quick start) and upload the generated `*.joblib` file via the demo UI.
  - Dependency or import errors on deploy: ensure the repository has a top-level `requirements.txt` (present) and the Streamlit app path is configured to `demo/streamlit_app.py` in Streamlit Cloud settings.

