#!/bin/sh
docker build \
  --load \
  -f /app/Dockerfile.celeryworker \
  --build-arg ENVIRONMENT=local \
  -t celeryworker:latest \
  --progress plain \
  /app
