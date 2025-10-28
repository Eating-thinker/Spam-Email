import os
import shutil
from ml.train_baseline import train_and_evaluate


def test_train_smoke(tmp_path):
    data = os.path.join(os.path.dirname(__file__), "..", "data", "sample_sms.csv")
    out = tmp_path / "results"
    model_path, metrics = train_and_evaluate(str(data), str(out), max_features=100, seed=1)
    assert os.path.exists(model_path)
    assert "accuracy" in metrics
