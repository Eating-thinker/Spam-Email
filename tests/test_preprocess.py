from ml.preprocess import clean_text, load_csv
import os


def test_clean_text():
    assert clean_text("Hello, WORLD!!") == "hello world"


def test_load_csv_sample(tmp_path):
    # use the included data/sample_sms.csv
    here = os.path.dirname(__file__)
    sample = os.path.join(here, "..", "data", "sample_sms.csv")
    X, y = load_csv(sample)
    assert len(X) >= 3
    assert set(y) <= {0, 1}
