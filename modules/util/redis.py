__author__ = 'tinglev@kth.se'

import json
import logging
import redis
from modules.util import exceptions

LOG = logging.getLogger(__name__)

def get_client(redis_url):
    try:
        return redis.StrictRedis(redis_url)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt create redis client. Error was: "{str(redis_err)}"')

def execute_json_set(client, key, value):
    try:
        LOG.debug('Writing key "%s" and value "%s"', key, value)
        client.execute_command('JSON.SET', key, '.', json.dumps(value))
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis set cmd. Error was: "{str(redis_err)}"')

def execute_json_get(client, key):
    try:
        LOG.debug('Getting key "%s"', key)
        value = client.execute_command('JSON.GET', key)
        if value:
            return json.loads(value)
        return value
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis get cmd. Error was: "{str(redis_err)}"')

def execute_json_delete(client, key):
    try:
        LOG.debug('Deleting key "%s"', key)
        return client.execute_command('JSON.DEL', key)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis delete cmd. Error was: "{str(redis_err)}"')
