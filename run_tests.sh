#!/bin/sh

# Start local reJSON
docker run -d -p 6379:6379 --name redis-rejson redislabs/rejson:latest

# Stack mock API server
FLASK_APP=mock_api.py pipenv run flask run &
MOCK_API_PID=$!

# Run with "--debug" to show program logs
REDIS_URL=localhost pipenv run green -vv --run-coverage --failfast "test/test_complete_pipeline.py" "$@"
if [ $? -eq 0 ]; then
    # Only run unit tests if the complete pipeline tests succeeded
    REDIS_URL=localhost pipenv run green -vv --run-coverage --failfast "test/unit" "$@"
fi

# Kill mock API server
kill $MOCK_API_PID 

# Stop and remove reJSON
docker stop redis-rejson
docker rm -f redis-rejson