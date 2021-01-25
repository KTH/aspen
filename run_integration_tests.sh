#!/bin/sh

# Start local redis
docker run -d -p 6379:6379 --name redis redis:latest

# Stack mock API server
FLASK_APP=mock_api.py pipenv run flask run &
MOCK_API_PID=$!

# Run with "--debug" to show program logs
REDIS_URL=localhost pipenv run green -vv --run-coverage --failfast --file-pattern "integration_*" "test/integration" "$@"

# Kill mock API server
kill $MOCK_API_PID 

# Stop and remove redis
docker stop redis
docker rm -f redis