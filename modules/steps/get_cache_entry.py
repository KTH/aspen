__author__ = 'tinglev@kth.se'

import json
import redis
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs, exceptions

class GetCacheEntry(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        redis_url = environment.get_with_default_string('REDIS_URL', 'redis')
        redis_client = self.redis_create_client(redis_url)
        file_path = pipeline_data[data_defs.STACK_FILE_PATH]
        cache_entry = self.redis_execute_cmd(redis_client, 'JSON.GET', file_path)
        self.log.debug('Got cache entry "%s"', cache_entry)
        if cache_entry:
            cache_entry = json.loads(cache_entry)
        pipeline_data[data_defs.CACHE_ENTRY] = cache_entry
        return pipeline_data

    def redis_create_client(self, redis_url):
        try:
            return redis.StrictRedis(redis_url)
        except redis.RedisError as redis_err:
            raise exceptions.DeploymentError(f'Couldnt connect to redis. Error was: "{str(redis_err)}"')

    def redis_execute_cmd(self, client, cmd, value):
        try:
            return client.execute_command(cmd, value)
        except redis.RedisError as redis_err:
            raise exceptions.DeploymentError(f'Couldnt execute redis cmd. Error was: "{str(redis_err)}"')
