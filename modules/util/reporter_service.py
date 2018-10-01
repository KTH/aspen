__author__ = 'tinglev@kth.se'

import redis
from modules.util import environment, exceptions, data_defs

# Hint type
def handle_error(error: exceptions.DeploymentError):
    if not error.reportable:
        return
    pipeline_data = error.pipeline_data
    application_name = pipeline_data[data_defs.APPLICATION_NAME]
    cluster_name = pipeline_data[data_defs.APPLICATION_CLUSTER]
    error_cache_key = f'{cluster_name}.{application_name}'
    redis_url = environment.get_with_default_string('REDIS_URL', 'redis')
    redis_client = redis_create_client(redis_url)
    result = redis_execute_cmd(redis_client, 'JSON.GET', error_cache_key)
    if result and result['step_name'] == error.step_name:
        # This error has already been reported
        pass
    else:
        # Repot to dizin
        pass
    raise error

def redis_create_client(redis_url):
    try:
        return redis.StrictRedis(redis_url)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt connect to redis. Error was: "{str(redis_err)}"')

def redis_execute_cmd(client, cmd, value):
    try:
        return client.execute_command(cmd, value)
    except redis.RedisError as redis_err:
        raise exceptions.DeploymentError(f'Couldnt execute redis cmd. Error was: "{str(redis_err)}"')