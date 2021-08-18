#!/bin/bash

set -e

# Build prod Docker image and push to Docker repo
echo "${DOCKER_PASS}" | docker login --username "${DOCKER_USER}" --password-stdin
docker build --target prod --tag "${DOCKER_USER}"/todo_app:latest --tag "${DOCKER_USER}"/todo_app:"${TRAVIS_COMMIT}" .
docker push "${DOCKER_USER}"/todo_app

# Push same image to Heroku repo
docker tag "${DOCKER_USER}"/todo_app registry.heroku.com/"${HEROKU_APP}"/web
docker login --username=_ --password="${HEROKU_API_KEY}" registry.heroku.com
docker push registry.heroku.com/"${HEROKU_APP}"/web

# Release/Deploy to Heroku
heroku container:release web -a "${HEROKU_APP}"