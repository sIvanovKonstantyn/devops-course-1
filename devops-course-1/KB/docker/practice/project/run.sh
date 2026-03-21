#!/bin/bash
# Enable error exit
set -e

# Build Docker images with BuildKit
DOCKER_BUILDKIT=1 docker compose build

# Start containers, rebuilding if necessary
docker compose up --build