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
