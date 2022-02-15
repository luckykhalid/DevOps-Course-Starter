#!/bin/bash

# Stop the execution of the script if a command has an error
set -e

# Build prod Docker image and push to Docker repo
echo "${DOCKER_PASS}" | docker login --username "${DOCKER_USER}" --password-stdin
docker build --target prod --tag "${DOCKER_USER}"/todo_app:latest --tag "${DOCKER_USER}"/todo_app:"${TRAVIS_COMMIT}" .
docker push "${DOCKER_USER}"/todo_app

# Notify Azure to get latest docker image and restart the app
curl -dH -X POST "$(terraform output -raw webhook_url)" --fail
#curl -dH -X POST "${WEBHOOK_URL}" --fail