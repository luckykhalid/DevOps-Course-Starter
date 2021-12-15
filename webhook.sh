#!/bin/bash

# Stop the execution of the script if a command has an error
set -e

curl -dH -X POST "${WEBHOOK_URL}" --fail