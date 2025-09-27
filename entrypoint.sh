#!/bin/sh
# exit on error
set -eu

echo "Running database migrations..."
flask db upgrade

echo "Starting Flask app..."
exec python3 -m flask --app app.py run

#run test inside of docker image
#exec pytest tests/ -vv --html=report.html --self-contained-html