__author__ = 'tinglev@kth.se'

import datetime
import logging
from os import pipe
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from modules.util import data_defs, redis, exceptions, environment

def create_cache_entry(step_name):
    return {
        'step_name': step_name,
        'reported_at': str(get_now())
    }

def get_cache_key(pipeline_data):
    mgt_res_grp = environment.get_env(environment.MANAGEMENT_RES_GRP)
    file_path = pipeline_data[data_defs.STACK_FILE_PATH]
    return f'error/{mgt_res_grp}/{file_path.lstrip("/")}' 

def write_to_error_cache(error: exceptions.DeploymentError):
    pipeline_data = error.pipeline_data
    cache_key = get_cache_key(pipeline_data)
    cache_entry = create_cache_entry(error.step_name)
    redis_client = redis.get_client()
    redis.execute_json_set(redis_client, cache_key, cache_entry)

def has_cached_error(error):
    pipeline_data = error.pipeline_data
    error_cache_key = get_cache_key(pipeline_data)
    result = get_error_cache(error_cache_key)
    if result and result['step_name'] == error.step_name:
        return result
    return None

def should_be_reported_again(error_cache_entry):
    last_reported_at = parse(error_cache_entry['reported_at'])
    report_again_at = last_reported_at + relativedelta(minutes=+10)
    return get_now() > report_again_at

def get_error_cache(error_cache_key):
    redis_client = redis.get_client()
    return redis.execute_json_get(redis_client, error_cache_key)

def get_now():
    # To simplify mocking in tests
    return datetime.datetime.now()
