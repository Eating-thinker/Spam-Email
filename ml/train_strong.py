"""Stronger training pipeline: uses TF-IDF (word + char n-grams) and GridSearchCV
to tune LogisticRegression and RandomForestClassifier. Saves best model and report.
"""
import json
import os
from pathlib import Path
from typing import Tuple

import joblib
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from ml.preprocess import load_csv, train_test_split_data


def download_if_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        r = requests.get(path, timeout=60)
        r.raise_for_status()
        tmp = Path("data")
        tmp.mkdir(parents=True, exist_ok=True)
        out = tmp / "downloaded_dataset.csv"
        out.write_bytes(r.content)
        return str(out)
    return path


def train_strong(data_path: str, out_dir: str, seed: int = 42, n_jobs: int = 1) -> Tuple[str, dict]:
    data_path = download_if_url(data_path)
    X, y = load_csv(data_path)
    X_train, X_test, y_train, y_test = train_test_split_data(X, y, seed=seed)

    # pipeline: tfidf -> classifier
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, max_features=20000)),
        ("clf", LogisticRegression(max_iter=2000, random_state=seed)),
    ])

    param_grid = [
        {
            "tfidf__ngram_range": [(1, 1), (1, 2)],
            "tfidf__analyzer": ["word", "char"],
            "clf": [LogisticRegression(max_iter=2000, random_state=seed, class_weight="balanced")],
            "clf__C": [0.01, 0.1, 1.0, 10.0],
        },
        {
            "tfidf__ngram_range": [(1, 2)],
            "tfidf__analyzer": ["word"],
            "clf": [RandomForestClassifier(random_state=seed, class_weight="balanced")],
            "clf__n_estimators": [100, 300],
            "clf__max_depth": [None, 20],
        },
    ]

    gs = GridSearchCV(pipe, param_grid, cv=5, scoring="f1", n_jobs=n_jobs, verbose=1)
    gs.fit(X_train, y_train)

    best = gs.best_estimator_
    preds = best.predict(X_test)

    acc = accuracy_score(y_test, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, preds, average="binary", zero_division=0)
    cm = confusion_matrix(y_test, preds).tolist()

    os.makedirs(out_dir, exist_ok=True)
    model_path = os.path.join(out_dir, "spam_best_model.joblib")
    joblib.dump({"model": best}, model_path)

    report = {
        "best_params": gs.best_params_,
        "accuracy": acc,
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "confusion_matrix": cm,
    }
    with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return model_path, report


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True, help="Path or URL to CSV dataset")
    p.add_argument("--out", required=True, help="Output dir for model and report")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--jobs", type=int, default=1)
    args = p.parse_args()

    model_path, report = train_strong(args.data, args.out, seed=args.seed, n_jobs=args.jobs)
    print(f"Saved model to {model_path}")
    print(report)
