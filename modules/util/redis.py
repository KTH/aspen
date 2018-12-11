"""redis.py

Util module for working with the redis cache"""

__author__ = 'tinglev@kth.se'

import json
import logging
import redis
from modules.util import exceptions, environment

LOG = logging.getLogger(__name__)

def get_client():
    try:
        redis_url = environment.get_with_default_string(environment.REDIS_URL, 'redis')
        return redis.StrictRedis(redis_url)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt create redis client. Error was: '
                                         f'"{str(redis_err)}"')

def delete_entire_cache():
    try:
        LOG.debug('Deleting entire redis cache')
        client = get_client()
        client.flushdb()
    except redis.RedisError as redis_err:
        raise exceptions.AspenError(f'Couldnt delete redis cache. Error was: '
                                    f'"{str(redis_err)}""')

def execute_json_set(client, key, value):
    try:
        LOG.debug('Writing key "%s" and value "%s"', key, value)
        client.execute_command('JSON.SET', key, '.', json.dumps(value))
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis set cmd. '
                                         f'Error was: "{str(redis_err)}"')

def execute_json_get(client, key):
    try:
        LOG.debug('Getting key "%s"', key)
        value = client.execute_command('JSON.GET', key)
        if value:
            return json.loads(value)
        return value
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis get cmd. '
                                         f'Error was: "{str(redis_err)}"')

def execute_json_delete(client, key):
    try:
        LOG.debug('Deleting key "%s"', key)
        return client.execute_command('JSON.DEL', key)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis delete cmd. '
                                         f'Error was: "{str(redis_err)}"')

def execute_command(client, command):
    try:
        LOG.debug('Running command "%s"', command)
        return client.execute_command(command)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis command f{command}. '
                                         f'Error was: "{str(redis_err)}"')

def clear_cache_with_filter(client, key_filter):
    keys = execute_command(client, f'KEYS *{key_filter}*')
    LOG.info('Found %s keys to clear', len(keys))
    for key in keys:
        execute_json_delete(client, key)
