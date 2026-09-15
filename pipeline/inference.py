import pickle
import numpy as np
from pathlib import Path
from sklearn.datasets import load_iris

MODEL_DIR = Path("models")


def load_latest_model():
    """Load latest model version."""
    pkl_files = sorted(MODEL_DIR.glob("model_v*.pkl"))
    if not pkl_files:
        raise FileNotFoundError("No trained model found")
    
    with open(pkl_files[-1], "rb") as f:
        return pickle.load(f)


def run_inference(model=None):
    """Run inference on test data."""
    if model is None:
        model = load_latest_model()
    
    X, y = load_iris(return_X_y=True)
    predictions = model.predict(X[:10])
    probabilities = model.predict_proba(X[:10])
    
    results = {
        "predictions": predictions.tolist(),
        "probabilities": probabilities.tolist(),
        "sample_count": len(predictions),
    }
    
    return results


if __name__ == "__main__":
    results = run_inference()
    print(f"Inference complete: {results['sample_count']} samples processed")
    print(f"Predictions: {results['predictions']}")
