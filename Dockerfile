FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY setup.py .
RUN pip install --no-cache-dir -e .

# Copy source
COPY pipeline/ pipeline/
COPY dags/ dags/

# Default: run training
CMD ["python", "-m", "pipeline.train"]
