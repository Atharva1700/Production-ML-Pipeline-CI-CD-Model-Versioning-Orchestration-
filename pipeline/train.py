import mlflow
import mlflow.sklearn
import pickle
import json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from pathlib import Path

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)


def train_model(experiment_name="iris-classifier"):
    """Train and log model to MLflow."""
    mlflow.set_experiment(experiment_name)
    
    # Load data
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    with mlflow.start_run():
        # Train
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        
        # Log
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")
        
        # Save locally for inference
        model_path = MODEL_DIR / f"model_v{mlflow.active_run().info.run_number}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        
        # Save metrics for CI/CD gate
        metrics_file = MODEL_DIR / "latest_metrics.json"
        with open(metrics_file, "w") as f:
            json.dump({"accuracy": accuracy, "f1": f1}, f)
        
        return accuracy, f1


if __name__ == "__main__":
    acc, f1 = train_model()
    print(f"Training complete: accuracy={acc:.3f}, f1={f1:.3f}")
