"""CLI wrapper to run the spam baseline training pipeline."""
from argparse import ArgumentParser
from ml.train_baseline import train_and_evaluate


def main():
    p = ArgumentParser()
    p.add_argument("--data", required=True, help="Path or URL to CSV dataset")
    p.add_argument("--out", required=True, help="Output directory")
    p.add_argument("--max-features", type=int, default=5000)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    model_path, metrics = train_and_evaluate(args.data, args.out, max_features=args.max_features, seed=args.seed)
    print(f"Trained model: {model_path}")
    print(metrics)


if __name__ == "__main__":
    main()
