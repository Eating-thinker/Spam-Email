Spam classification ML pipeline

Quick start

1. Install dependencies: `pip install -r ml/requirements.txt`
2. Run the baseline training on a dataset (path or URL):

```
python ml/train_baseline.py --data data/sms_spam_no_header.csv --out ml/results/
```

For small smoke runs use the included `data/sample_sms.csv`.
