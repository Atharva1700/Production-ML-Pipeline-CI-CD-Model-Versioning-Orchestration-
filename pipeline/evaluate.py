import json
import sys
from pathlib import Path

MODEL_DIR = Path("models")
METRICS_THRESHOLD = {"accuracy": 0.90, "f1_score": 0.88}


def evaluate_for_promotion():
    """Check if model meets promotion criteria."""
    metrics_file = MODEL_DIR / "latest_metrics.json"
    
    if not metrics_file.exists():
        print("❌ No metrics found")
        return False
    
    with open(metrics_file) as f:
        metrics = json.load(f)
    
    passed = True
    for metric, threshold in METRICS_THRESHOLD.items():
        value = metrics.get(metric.replace("_score", ""), 0)
        status = "✅" if value >= threshold else "❌"
        print(f"{status} {metric}: {value:.3f} (threshold: {threshold:.3f})")
        if value < threshold:
            passed = False
    
    return passed


if __name__ == "__main__":
    if evaluate_for_promotion():
        print("\n✅ Model APPROVED for production")
        sys.exit(0)
    else:
        print("\n❌ Model REJECTED: thresholds not met")
        sys.exit(1)
