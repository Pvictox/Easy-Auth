#!/bin/bash

echo "Starting FastAPI Auth Project..."
while ! nc -z db 5432; do
  echo "Waiting for POSTGRES database..."
  sleep 1
done

echo "POSTGRES database is up - starting application"

echo "Applying database migrations..."
alembic upgrade head


if [ "$ENVIRONMENT" = "development" ]; then #Defined in docker-compose-dev.yml or docker-compose-prod.yml
    echo "Running FASTAPI in development mode..."
    fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload
else
    echo "Running FASTAPI in production mode..."
    fastapi run app/main.py --host 0.0.0.0 --port 8000
fi
