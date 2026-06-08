# =============================================================================
# Dockerfile for the Django 'core' service
# Supports both local/development and production environments
# via the ARG ENVIRONMENT build argument.
#
# Usage:
#   Local:      docker build --build-arg ENVIRONMENT=local -t core:local .
#   Production: docker build --build-arg ENVIRONMENT=production -t core:prod .
# =============================================================================

# -----------------------------------------------------------------------------
# Base image: Python 3.9.13 (pinned for reproducibility)
# -----------------------------------------------------------------------------
FROM python:3.9.13

# -----------------------------------------------------------------------------
# Build argument to switch between environments:
#   local       → installs dev dependencies + telnet, runs Django dev server
#   production  → installs prod dependencies only, runs Gunicorn
# -----------------------------------------------------------------------------
ARG ENVIRONMENT=local

# -----------------------------------------------------------------------------
# Environment variables:
#   PYTHONUNBUFFERED  → forces stdout/stderr to be unbuffered (better logging)
#   PIP_NO_CACHE_DIR  → disables pip cache to reduce image size
#   PIP_DISABLE_PIP_VERSION_CHECK → suppresses pip upgrade warnings
#   ENVIRONMENT       → makes the build ARG available at runtime for CMD logic
# -----------------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ENVIRONMENT=${ENVIRONMENT}

# -----------------------------------------------------------------------------
# Set the working directory for all subsequent instructions
# -----------------------------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------------------------
# Copy only the requirements files first to leverage Docker layer caching.
# Dependencies are re-installed only when requirements files change.
# -----------------------------------------------------------------------------
COPY requirements/*.txt /tmp/requirements/

# -----------------------------------------------------------------------------
# Install system and Python dependencies based on the target environment.
#
# buildDeps  → required to compile native Python extensions (e.g. psycopg2)
# runDeps    → required at runtime (git)
# localDeps  → useful for local debugging only (telnet)
#
# In production: build deps are removed after pip install to reduce image size.
# -----------------------------------------------------------------------------
RUN set -x \
    && buildDeps="build-essential" \
    && runDeps="git" \
    && localDeps="telnet" \
    # Update apt package index
    && apt-get update \
    # Install build-time dependencies (needed to compile psycopg2, etc.)
    && apt-get install -y --no-install-recommends $buildDeps \
    # Install runtime dependencies
    && apt-get install -y --no-install-recommends $runDeps \
    # Environment-specific Python dependency installation
    && if [ "$ENVIRONMENT" = "local" ] || [ "$ENVIRONMENT" = "development" ]; then \
        # Install local debugging tools
        apt-get install -y --no-install-recommends $localDeps \
        # Install local/development Python dependencies (includes debug toolbar, etc.)
        && pip install -r /tmp/requirements/local.txt; \
    else \
        # Install production Python dependencies only (gunicorn, no debug tools)
        pip install -r /tmp/requirements/production.txt \
        # Remove build dependencies to keep the production image lean
        && apt-get remove -y $buildDeps \
        && apt-get autoremove -y; \
    fi \
    # Clean up apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Remove temporary requirements files
    && rm -rf /tmp/*

# -----------------------------------------------------------------------------
# Copy the full application source code into the container.
# Done after dependency installation to maximise Docker layer cache reuse.
# -----------------------------------------------------------------------------
COPY . .

# -----------------------------------------------------------------------------
# Ensure the entrypoint script is executable.
# The entrypoint handles:
#   1. Waiting for PostgreSQL to be ready (via psycopg2 health check)
#   2. Running makemigrations and migrate
#   3. Loading initial data if this is the first run
#   4. Starting the Django development server
# -----------------------------------------------------------------------------
RUN chmod +x /app/docker-entrypoint.sh

# -----------------------------------------------------------------------------
# Startup command:
#   local/development → runs docker-entrypoint.sh (dev server on port 8000)
#   production        → runs Gunicorn WSGI server directly (multi-worker)
#                       Note: In production, DB migrations should be handled
#                       separately (e.g. init container or CI/CD pipeline).
# -----------------------------------------------------------------------------
CMD if [ "$ENVIRONMENT" = "production" ]; then \
        gunicorn core.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers 2 \
            --timeout 120 \
            --log-level info; \
    else \
        /app/docker-entrypoint.sh; \
    fi
