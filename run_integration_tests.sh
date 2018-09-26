#!/bin/sh

# Start local reJSON
docker run -d -p 6379:6379 --name redis-rejson redislabs/rejson:latest

# Run with "--debug" to show program logs
REDIS_URL=localhost pipenv run green -vv --run-coverage --failfast --file-pattern "integration_*" "tests/integration" "$@"

docker stop redis-rejson
docker rm -f redis-rejson