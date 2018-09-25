#!/bin/sh

# Run with "--debug" to show program logs
pipenv run green -vv --run-coverage --failfast "tests" "$@"
