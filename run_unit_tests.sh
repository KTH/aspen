#!/bin/sh

# Start local reJSON
if [ "$1" != "docker" ]; then
    docker run -d -p 6379:6379 --name redis-rejson redislabs/rejson:latest
    REDIS_URL=localhost
else
    pipenv install --dev --pre
    REDIS_URL=redis-rejson
fi

# Stack mock API server
FLASK_APP=mock_api.py pipenv run flask run &
MOCK_API_PID=$!

REDIS_URL=$REDIS_URL pipenv run green -vv --run-coverage --failfast "test/unit" "$@"

# Kill mock API server
kill $MOCK_API_PID 

# Stop and remove reJSON
if [ "$1" != "docker" ]; then
    docker stop redis-rejson
    docker rm -f redis-rejson
fi