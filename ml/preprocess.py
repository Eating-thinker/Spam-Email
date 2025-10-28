import csv
import re
from typing import List, Tuple
import pandas as pd
from sklearn.model_selection import train_test_split


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    txt = text.lower()
    txt = re.sub(r"[^a-z0-9\s]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def load_csv(path: str) -> Tuple[List[str], List[str]]:
    # The dataset may have no header and two columns: label, text
    df = pd.read_csv(path, header=None, encoding="utf-8", names=["label", "text"])
    df = df.dropna(subset=["text"])  # drop malformed rows
    X = df["text"].astype(str).map(clean_text).tolist()
    y = df["label"].astype(str).map(lambda v: 1 if v.lower().startswith("spam") else 0).tolist()
    return X, y


def train_test_split_data(X: List[str], y: List[int], test_size: float = 0.2, seed: int = 42):
    # Handle small-sample edge cases: scikit-learn's stratify requires at least
    # 2 samples per class in the test/train split. If dataset is tiny, compute
    # an integer test_size that ensures at least one example per class in test
    # where possible.
    n = len(y)
    classes = set(y)
    n_classes = len(classes)
    if n == 0:
        return [], [], [], []

    # If float, convert to int number of test samples
    if isinstance(test_size, float):
        n_test = max(1, int(n * test_size))
    else:
        n_test = int(test_size)

    if n_test < n_classes:
        # ensure test contains at least one example per class when possible
        n_test = n_classes

    # If n_test equals n (or too large), fall back to 1 sample test
    if n_test >= n:
        n_test = max(1, n - n_classes)

    return train_test_split(X, y, test_size=n_test, random_state=seed, stratify=y)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("data", help="Path to CSV dataset")
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    X, y = load_csv(args.data)
    X_train, X_test, y_train, y_test = train_test_split_data(X, y, test_size=args.test_size, seed=args.seed)
    print(f"Loaded {len(X)} rows. Train: {len(X_train)} Test: {len(X_test)}")
