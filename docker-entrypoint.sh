#!/usr/bin/env bash

# bash options

set -o errexit
set -o nounset

# basic funtions

function log {
  local -r level="$1"
  shift
  local -ra message=("$@")
  local -r timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  local -r scriptname="$(basename "$0")"

  >&2 echo -e "${timestamp} [${level}] [$scriptname] ${message[*]}"
}

function log_info {
  local -ra message=("$@")
  log "INFO" "${message[@]}"
}

function log_warn {
  local -ra message=("$@")
  log "WARN" "${message[@]}"
}

function log_error {
  local -ra message=("$@")
  log "ERROR" "${message[@]}"
}

if [ -z "${DB_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi
export DATABASE_URL="postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

# health of dependent services

postgres_ready() {
    python << END
import sys
from psycopg2 import connect
from psycopg2.errors import OperationalError
try:
    connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
    )
except OperationalError:
    sys.exit(-1)
END
}

until postgres_ready; do
  log_info "Waiting for PostgreSQL to become available"
  sleep 5
done
  log_info "PostgreSQL is available"

# idempotent Django commands

log_info "[run] make migrations"
python manage.py makemigrations || exit 1

log_info "[run] Migrate DB"
python manage.py migrate || exit 1



INITIAL_RUN_CHECK=$(python manage.py shell -c "from apps.user.models import User; print(User.objects.filter(is_superuser=True).exists())")
if [  "${INITIAL_RUN_CHECK}" == "False" ]; then
  log_info "[run] Load initial data"
  # Example
  # python manage.py loaddata initial_data.json || exit 1
fi

python manage.py runserver 0.0.0.0:8000