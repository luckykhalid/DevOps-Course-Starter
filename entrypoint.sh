#!/bin/bash

# run the app using gunicorn
poetry run gunicorn -b "0.0.0.0:${PORT:-5000}" "todo_app.app:create_app()"