#!/bin/bash
set -e

MONGO_STARTED=false

if nc -z localhost 27017 2>/dev/null; then
  echo "MongoDB already running on port 27017, skipping docker run."
else
  echo "Starting MongoDB container..."
  docker run -d --rm --name nodegoat-mongo -p 27017:27017 mongo:4.4
  MONGO_STARTED=true
  echo "Waiting for MongoDB to be ready..."
  timeout 30s bash -c 'until nc -z localhost 27017; do sleep 1; done'
fi

npm run db:seed

npm run test:ci
EXIT_CODE=$?

if [ "$MONGO_STARTED" = true ]; then
  echo "Stopping MongoDB container..."
  docker stop nodegoat-mongo
fi

exit $EXIT_CODE
