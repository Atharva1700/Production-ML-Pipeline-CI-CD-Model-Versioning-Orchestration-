import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.train import train_model
from pipeline.inference import run_inference
from pipeline.evaluate import evaluate_for_promotion


def test_train_model():
    """Train model and verify metrics."""
    acc, f1 = train_model(experiment_name="test-iris")
    assert acc > 0.85, f"Accuracy too low: {acc}"
    assert f1 > 0.85, f"F1 score too low: {f1}"


def test_inference():
    """Run inference after training."""
    results = run_inference()
    assert "predictions" in results
    assert results["sample_count"] > 0
    assert len(results["predictions"]) == results["sample_count"]


def test_evaluate_gate():
    """Evaluate model promotion gate."""
    # Should pass if trained model meets thresholds
    result = evaluate_for_promotion()
    assert isinstance(result, bool)
