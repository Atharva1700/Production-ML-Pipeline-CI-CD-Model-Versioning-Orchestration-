from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import sys

sys.path.insert(0, "/opt/airflow")

from pipeline.train import train_model
from pipeline.evaluate import evaluate_for_promotion
from pipeline.inference import run_inference

default_args = {
    "owner": "ml-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": days_ago(1),
}

with DAG(
    "ml_pipeline",
    default_args=default_args,
    description="End-to-end ML pipeline: train → evaluate → inference",
    schedule_interval="0 2 * * *",  # Daily at 2 AM
    catchup=False,
) as dag:
    
    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
        op_kwargs={"experiment_name": "iris-classifier"},
    )
    
    evaluate = PythonOperator(
        task_id="evaluate_gate",
        python_callable=evaluate_for_promotion,
    )
    
    inference = PythonOperator(
        task_id="run_inference",
        python_callable=run_inference,
    )
    
    # Pipeline: train → evaluate gate → inference only if approved
    train >> evaluate >> inference
