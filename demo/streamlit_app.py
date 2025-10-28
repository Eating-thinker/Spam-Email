import json
from pathlib import Path

import joblib
import streamlit as st


@st.cache_resource
def load_model(path: str):
    data = joblib.load(path)
    # model stored as dict { 'model': Pipeline }
    return data.get("model") if isinstance(data, dict) else data


def predict_text(model, text: str):
    pred = model.predict([text])[0]
    prob = None
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba([text])[0].tolist()
    return int(pred), prob


def main():
    st.title("Spam Email Classification — Demo")
    st.write("Upload a trained model (joblib) or use the default sample model if present in `ml/results/`.")

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

    text = st.text_area("Enter email or SMS text to classify:")
    if st.button("Predict"):
        if not model:
            st.error("No model available")
            return
        pred, prob = predict_text(model, text)
        st.write("Prediction:", "SPAM" if pred == 1 else "HAM (not spam)")
        if prob is not None:
            st.write("Probabilities:", prob)

    st.markdown("---")
    st.write("Batch predict: upload a CSV with two columns (label,text) without header. Output will be predictions in a JSON lines file.")
    csv_file = st.file_uploader("Upload batch CSV", type=["csv"]) 
    if csv_file is not None and st.button("Run batch prediction"):
        if not model:
            st.error("No model available")
            return
        import pandas as pd

        df = pd.read_csv(csv_file, header=None, names=["label", "text"], encoding="utf-8")
        preds = model.predict(df["text"].astype(str).tolist())
        df["pred"] = preds
        out = Path(".tmp")
        out.mkdir(exist_ok=True)
        outf = out / "predictions.jsonl"
        with open(outf, "w", encoding="utf-8") as f:
            for r in df.to_dict(orient="records"):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        st.success(f"Wrote predictions to {outf}")


if __name__ == "__main__":
    main()
