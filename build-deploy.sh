#!/bin/bash

# Stop the execution of the script if a command has an error
set -e

# Push same image to Heroku repo
docker tag "${DOCKER_USER}"/todo_app registry.heroku.com/"${HEROKU_APP}"/web
docker login --username=_ --password="${HEROKU_API_KEY}" registry.heroku.com
docker push registry.heroku.com/"${HEROKU_APP}"/web

# Release/Deploy to Heroku
#heroku container:release web -a "${HEROKU_APP}"