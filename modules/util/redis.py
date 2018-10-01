__author__ = 'tinglev@kth.se'

import redis
from modules.util import exceptions

def get_client(redis_url):
    try:
        return redis.StrictRedis(redis_url)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt create redis client. Error was: "{str(redis_err)}"')

def execute_json_set(client, key, value):
    try:
        client.execute_command('JSON.SET', key, '.', value)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis set cmd. Error was: "{str(redis_err)}"')

def execute_json_get(client, key):
    try:
        return client.execute_command('JSON.GET', key)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis get cmd. Error was: "{str(redis_err)}"')

def execute_json_delete(client, key):
    try:
        return client.execute_command('JSON.DEL', key)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis delete cmd. Error was: "{str(redis_err)}"')
