# Production ML Pipeline

End-to-end ML pipeline with Airflow orchestration, MLflow versioning, Docker containerization, and CI/CD automation.

## Architecture

```
train (Airflow) → MLflow (log metrics/model) → evaluate gate → inference
     ↓                                              ↓
  RandomForest                                  Promotion check
  (Iris dataset)                                (accuracy ≥ 90%)
```

## Quick Start

### Local (standalone)
```bash
pip install -e .
python -m pipeline.train          # Train model
python -m pipeline.evaluate       # Check promotion gate
python -m pipeline.inference      # Run inference
```

### Docker Compose (full stack)
```bash
docker-compose up
```

Then:
- **Airflow UI**: http://localhost:8080 (admin/admin)
- **MLflow UI**: http://localhost:5000
- **Postgres**: localhost:5432

### Trigger pipeline in Airflow
```bash
curl -X POST http://localhost:8080/api/v1/dags/ml_pipeline/dagRuns
```

## File Structure

```
├── pipeline/              # Core ML code
│   ├── train.py          # Training logic + MLflow logging
│   ├── inference.py      # Model inference
│   └── evaluate.py       # Promotion gate (accuracy/F1 thresholds)
├── dags/
│   └── ml_pipeline.py    # Airflow DAG orchestration
├── tests/
│   └── test_pipeline.py  # Unit tests
├── .github/workflows/
│   └── ci-cd.yml         # GitHub Actions CI/CD
├── docker-compose.yml    # Local dev stack
├── Dockerfile            # Container image
├── config.yaml           # Pipeline configuration
└── setup.py              # Python package
```

## Key Features

1. **MLflow Integration**
   - Automatic model versioning and metric tracking
   - Experiment management
   - Model registry for production deployment

2. **Airflow Orchestration**
   - Scheduled daily training (2 AM)
   - Task dependency management
   - Automatic retries on failure

3. **CI/CD Gate**
   - Automated model evaluation
   - Threshold-based promotion (accuracy ≥ 90%, F1 ≥ 88%)
   - Blocks promotion if metrics don't meet standards

4. **Docker**
   - Containerized training and inference
   - docker-compose for full stack local development
   - GitHub Actions automated builds

5. **Testing**
   - Unit tests for all components
   - Integrated into CI/CD pipeline
   - Run tests before model training

## Configuration

Edit `config.yaml` to adjust:
- MLflow tracking server
- Model hyperparameters
- Evaluation thresholds
- Airflow scheduling

## Production Deployment

1. Push to main branch
2. CI/CD pipeline runs: tests → train → evaluate → build Docker image
3. If evaluation passes, image is ready for deployment
4. Deploy container to production orchestrator (K8s, ECS, etc.)

## Monitoring

- **Airflow**: Monitor task runs and failures in web UI
- **MLflow**: Track metrics, compare models, promote to staging/prod
- **Logs**: Check `/opt/airflow/logs/` in Docker or local directory

## Troubleshooting

**Port conflicts?** Change in docker-compose.yml:
```yaml
ports:
  - "8081:8080"  # Airflow on 8081 instead
```

**Model not training?** Check MLflow connection:
```bash
curl http://localhost:5000/health
```

**Evaluation gate failing?** Adjust thresholds in `config.yaml` or `pipeline/evaluate.py`.
