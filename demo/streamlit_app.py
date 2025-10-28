import json
from pathlib import Path

import os
import sys
import joblib
import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

# Ensure the repository root is on sys.path so `ml` can be imported on hosted
# environments (e.g., Streamlit Cloud) where the package is not installed.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ml.preprocess import clean_text


@st.cache_resource
def load_model(path: str):
    data = joblib.load(path)
    # model may be stored in different formats:
    # - a Pipeline or estimator object (callable with raw text)
    # - a dict with keys { 'vectorizer': vec, 'model': clf }
    return data


def predict_text(model, text: str):
    # Support both Pipeline-like models and dict {vectorizer, model} saved artifacts
    if isinstance(model, dict):
        vec = model.get("vectorizer")
        clf = model.get("model")
        if vec is None or clf is None:
            raise ValueError("Model dict missing 'vectorizer' or 'model' keys")
        X = vec.transform([text])
        pred = clf.predict(X)[0]
        prob = clf.predict_proba(X)[0].tolist() if hasattr(clf, "predict_proba") else None
        return int(pred), prob
    else:
        pred = model.predict([text])[0]
        prob = None
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba([text])[0].tolist()
        return int(pred), prob


def main():
    st.title("Spam Email Classification — Demo")
    st.write("Upload a trained model (joblib) or use the default sample model if present in `ml/results_sample/`.")

    default_model = Path("ml/results_sample/spam_logreg.joblib")
    uploaded = st.file_uploader("Upload joblib model file", type=["joblib", "pkl"], accept_multiple_files=False)

    model = None
    if uploaded is not None:
        bytes_data = uploaded.read()
        Path(".tmp").mkdir(exist_ok=True)
        tmp_path = Path(".tmp") / uploaded.name
        tmp_path.write_bytes(bytes_data)
        model = load_model(str(tmp_path))
    elif default_model.exists():
        model = load_model(str(default_model))
    else:
        st.warning("No model found. Run training and place joblib in ml/results_sample/ or upload one.")

    st.header("Single text prediction")
    text = st.text_area("Enter email or SMS text to classify:", height=120)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Predict"):
            if not model:
                st.error("No model available")
            else:
                pred, prob = predict_text(model, text)
                st.markdown(f"**Prediction:** {'**SPAM**' if pred == 1 else 'HAM (not spam)'}")
                if prob is not None:
                    st.write("Probabilities:", prob)

    with col2:
        st.markdown("**Model status**")
        if model is None:
            st.write("No model loaded")
        else:
            st.write("Model loaded — you can upload a different model to try it.")

    st.markdown("---")
    st.header("Dataset viewer & training stats")
    st.write("Upload your dataset CSV (no header, two columns: label,text) or use the included sample to explore training data statistics.")
    ds_file = st.file_uploader("Upload dataset CSV (optional)", type=["csv"], key="dataset")

    df = None
    if ds_file is not None:
        try:
            df = pd.read_csv(ds_file, header=None, names=["label", "text"], encoding="utf-8")
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
    else:
        sample = Path("data/sample_sms.csv")
        if sample.exists():
            df = pd.read_csv(sample, header=None, names=["label", "text"], encoding="utf-8")

    if df is not None:
        st.subheader("Raw preview")
        st.dataframe(df.head(10))

        # Basic stats
        df = df.dropna(subset=["text"]).copy()
        df["label_norm"] = df["label"].astype(str).str.lower().map(lambda v: "spam" if v.startswith("spam") else "ham")
        st.write("Total rows:", len(df))

        counts = df["label_norm"].value_counts()
        st.subheader("Class distribution")
        st.bar_chart(counts)

        st.subheader("Message length distribution")
        df["len"] = df["text"].astype(str).map(lambda t: len(t))
        st.bar_chart(df["len"].value_counts().sort_index())

        st.subheader("Top tokens (by frequency)")
        toks = Counter()
        for t in df["text"].astype(str).tolist():
            for w in clean_text(t).split():
                toks[w] += 1
        top = toks.most_common(30)
        st.table(pd.DataFrame(top, columns=["token", "count"]).set_index("token"))

        st.subheader("Examples by class")
        ham_ex = df[df["label_norm"] == "ham"]["text"].head(3).tolist()
        spam_ex = df[df["label_norm"] == "spam"]["text"].head(3).tolist()
        st.markdown("**Ham examples**")
        for e in ham_ex:
            st.write(e)
        st.markdown("**Spam examples**")
        for e in spam_ex:
            st.write(e)

    st.markdown("---")
    st.write("Batch predict: upload a CSV with two columns (label,text) without header. Output will be predictions in a JSON lines file.")
    csv_file = st.file_uploader("Upload batch CSV for prediction", type=["csv"], key="batch") 
    if csv_file is not None and st.button("Run batch prediction"):
        if not model:
            st.error("No model available")
        else:
            df2 = pd.read_csv(csv_file, header=None, names=["label", "text"], encoding="utf-8")
            preds = None
            # handle dict vs pipeline
            if isinstance(model, dict):
                vec = model.get("vectorizer")
                clf = model.get("model")
                Xt = vec.transform(df2["text"].astype(str).tolist())
                preds = clf.predict(Xt)
            else:
                preds = model.predict(df2["text"].astype(str).tolist())
            df2["pred"] = preds
            out = Path(".tmp")
            out.mkdir(exist_ok=True)
            outf = out / "predictions.jsonl"
            with open(outf, "w", encoding="utf-8") as f:
                for r in df2.to_dict(orient="records"):
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            st.success(f"Wrote predictions to {outf}")


if __name__ == "__main__":
    main()
