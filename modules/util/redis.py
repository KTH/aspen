"""redis.py

Util module for working with the redis cache"""

__author__ = 'tinglev@kth.se'

import json
import logging
import redis
from modules.util import exceptions, environment

def get_client():
    try:
        redis_url = environment.get_with_default_string(environment.REDIS_URL, 'redis')
        return redis.StrictRedis(redis_url)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt create redis client. Error was: '
                                         f'"{str(redis_err)}"')

def delete_entire_cache():
    try:
        logger = logging.getLogger(__name__)
        logger.debug('Deleting entire redis cache')
        client = get_client()
        client.flushdb()
    except redis.RedisError as redis_err:
        raise exceptions.AspenError(f'Couldnt delete redis cache. Error was: '
                                    f'"{str(redis_err)}""')

def execute_json_set(client, key, value):
    try:
        logger = logging.getLogger(__name__)
        logger.debug('Writing key "%s" and value "%s"', key, value)
        client.execute_command('JSON.SET', key, '.', json.dumps(value))
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis set cmd. '
                                         f'Error was: "{str(redis_err)}"')

def execute_json_get(client, key):
    try:
        logger = logging.getLogger(__name__)
        logger.debug('Getting key "%s"', key)
        value = client.execute_command('JSON.GET', key)
        if value:
            return json.loads(value)
        return value
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis get cmd. '
                                         f'Error was: "{str(redis_err)}"')

def execute_json_delete(client, key):
    try:
        logger = logging.getLogger(__name__)
        logger.debug('Deleting key "%s"', key)
        return client.execute_command('JSON.DEL', key)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis delete cmd. '
                                         f'Error was: "{str(redis_err)}"')

def execute_command(client, command):
    try:
        logger = logging.getLogger(__name__)
        logger.debug('Running command "%s"', command)
        return client.execute_command(command)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis command f{command}. '
                                         f'Error was: "{str(redis_err)}"')

def get_all_keys(client):
    keys = execute_command(client, f'KEYS *')
    return [key.decode("utf-8") for key in keys]

def clear_cache_with_filter(client, key_filter):
    logger = logging.getLogger(__name__)
    keys = execute_command(client, f'KEYS *{key_filter}*')
    logger.info('Found %s keys to clear', len(keys))
    for key in [key.decode("utf-8") for key in keys]:
        execute_json_delete(client, key)
