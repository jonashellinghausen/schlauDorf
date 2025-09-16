#!/usr/bin/env bash
set -euo pipefail

# Load environment variables from .env if available for production parity.
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

export FLASK_APP=${FLASK_APP:-run.py}
export FLASK_DEBUG=0

echo "Running database migrations..."
flask db upgrade

echo "Starting Gunicorn server..."
exec gunicorn --config gunicorn.conf.py "run:app"
