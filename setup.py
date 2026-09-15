from setuptools import setup
setup(
    name="ml-pipeline",
    version="1.0.0",
    packages=["pipeline"],
    install_requires=[
        "apache-airflow==2.7.3",
        "mlflow==2.10.2",
        "scikit-learn==1.3.2",
        "pandas==2.1.3",
        "numpy==1.24.3",
        "pydantic==2.5.0",
        "pyyaml==6.0.1",
    ],
)
