#!/bin/sh
# exit on error
set -euo pipefail

echo "Running database migrations..."
flask db upgrade

echo "Starting Flask app..."
exec python3 -m flask --app run_server run --host=0.0.0.0 --port=5000