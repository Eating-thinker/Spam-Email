import argparse
import json
import os
from pathlib import Path
from typing import Tuple

import joblib
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

from ml.preprocess import load_csv, train_test_split_data


def download_if_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        r = requests.get(path, timeout=30)
        r.raise_for_status()
        tmp = Path("data")
        tmp.mkdir(parents=True, exist_ok=True)
        out = tmp / "downloaded_dataset.csv"
        out.write_bytes(r.content)
        return str(out)
    return path


def train_and_evaluate(data_path: str, out_dir: str, max_features: int = 5000, seed: int = 42) -> Tuple[str, dict]:
    data_path = download_if_url(data_path)
    X, y = load_csv(data_path)
    X_train, X_test, y_train, y_test = train_test_split_data(X, y, seed=seed)

    vec = TfidfVectorizer(max_features=max_features)
    X_train_t = vec.fit_transform(X_train)
    X_test_t = vec.transform(X_test)

    clf = LogisticRegression(max_iter=1000, random_state=seed)
    clf.fit(X_train_t, y_train)

    preds = clf.predict(X_test_t)
    acc = accuracy_score(y_test, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, preds, average="binary", zero_division=0)
    cm = confusion_matrix(y_test, preds).tolist()

    os.makedirs(out_dir, exist_ok=True)
    model_path = os.path.join(out_dir, "spam_logreg.joblib")
    joblib.dump({"vectorizer": vec, "model": clf}, model_path)

    metrics = {"accuracy": acc, "precision": float(precision), "recall": float(recall), "f1": float(f1), "confusion_matrix": cm}
    with open(os.path.join(out_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return model_path, metrics


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True, help="Path or URL to CSV dataset")
    p.add_argument("--out", required=True, help="Output directory for model and metrics")
    p.add_argument("--max-features", type=int, default=5000)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    model_path, metrics = train_and_evaluate(args.data, args.out, max_features=args.max_features, seed=args.seed)
    print(f"Model saved to: {model_path}")
    print("Metrics:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
