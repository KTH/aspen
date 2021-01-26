#!/bin/sh

# Start local redis
if [ "$1" != "docker" ]; then
    docker run -d -p 6379:6379 --name redis redis:latest
    REDIS_URL=redis://localhost:6379
else
    pipenv install --dev --pre
    REDIS_URL=redis://redis:6379
fi

# Stack mock API server
FLASK_APP=mock_api.py pipenv run flask run &
MOCK_API_PID=$!

REDIS_URL=$REDIS_URL pipenv run green -vv --run-coverage --failfast "test/unit" "$@"

# Kill mock API server
kill $MOCK_API_PID 

# Stop and remove redis
if [ "$1" != "docker" ]; then
    docker stop redis
    docker rm -f redis
fi