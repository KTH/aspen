__author__ = 'tinglev@kth.se'

import json
import redis
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs

class GetCacheEntry(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        redis_url = environment.get_with_default_string('REDIS_URL', 'redis')
        redis_client = redis.StrictRedis(redis_url)
        file_path = pipeline_data[data_defs.STACK_FILE_PATH]
        cache_entry = redis_client.execute_command('JSON.GET', file_path)
        self.log.debug('Got cache entry "%s"', cache_entry)
        if cache_entry:
            cache_entry = json.loads(cache_entry)
        pipeline_data[data_defs.CACHE_ENTRY] = cache_entry
        return pipeline_data
