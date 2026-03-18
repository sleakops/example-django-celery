# ============================================================
# Dockerfile for the Django/Celery core service
# Supports: local, development, production environments
# Usage:
#   Local:      docker build --build-arg ENVIRONMENT=local -t core .
#   Production: docker build --build-arg ENVIRONMENT=production -t core .
# ============================================================

# Base image: Python 3.11 slim (LTS-aligned, amd64 compatible)
FROM python:3.11-slim

# ------------------------------------------------------------
# Build argument to switch between environments
# Values: local | development | production (default: local)
# ------------------------------------------------------------
ARG ENVIRONMENT=local

# ------------------------------------------------------------
# Environment variables for Python and pip behaviour
# ------------------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ENVIRONMENT=${ENVIRONMENT}

# ------------------------------------------------------------
# Set working directory
# ------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------
# Install system dependencies
#   - build-essential : needed to compile psycopg2 C extensions
#   - libpq-dev       : PostgreSQL client headers for psycopg2
#   - git             : required by some pip packages
#   - telnet          : useful for local debugging only
# In production, build-time deps are removed after pip install
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        git \
        $(if [ "$ENVIRONMENT" = "local" ] || [ "$ENVIRONMENT" = "development" ]; then echo "telnet"; fi) \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Copy only requirements files first (layer cache optimisation)
# ------------------------------------------------------------
COPY requirements/ /tmp/requirements/

# ------------------------------------------------------------
# Install Python dependencies based on the target environment
#   - local/development : requirements/local.txt (includes debug toolbar)
#   - production        : requirements/production.txt (includes gunicorn)
# ------------------------------------------------------------
RUN if [ "$ENVIRONMENT" = "local" ] || [ "$ENVIRONMENT" = "development" ]; then \
        pip install -r /tmp/requirements/local.txt; \
    else \
        pip install -r /tmp/requirements/production.txt; \
    fi \
    # Clean up temporary requirements files
    && rm -rf /tmp/requirements

# ------------------------------------------------------------
# Copy the full application source code into the container
# ------------------------------------------------------------
COPY . .

# ------------------------------------------------------------
# Copy and set permissions on the Docker entrypoint script
# The entrypoint handles:
#   - Waiting for PostgreSQL to be ready
#   - Running makemigrations and migrate
#   - Loading initial data (if needed)
# ------------------------------------------------------------
RUN chmod +x /app/docker-entrypoint.sh

# ------------------------------------------------------------
# Expose the application port
# ------------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------------
# Startup command:
#   - local/development : Django dev server (hot-reload)
#   - production        : Gunicorn WSGI server (multi-worker)
# The entrypoint script runs first to ensure DB readiness
# ------------------------------------------------------------
CMD if [ "$ENVIRONMENT" = "local" ] || [ "$ENVIRONMENT" = "development" ]; then \
        /app/docker-entrypoint.sh; \
    else \
        /app/docker-entrypoint.sh && \
        gunicorn core.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers 2 \
            --timeout 120 \
            --log-level info; \
    fi
