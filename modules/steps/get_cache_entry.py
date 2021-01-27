"""GetCacheEntry

Uses the docker-stack.yml path of this deployment to fetch
any deployment cache entry that exists in our redis instance"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.steps.write_cache_entry import get_cache_key
from modules.util import data_defs, redis

class GetCacheEntry(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        redis_client = redis.get_client()
        cache_key = get_cache_key(pipeline_data)
        cache_entry = redis.execute_json_get(redis_client, cache_key)
        self.log.debug('Got cache entry "%s"', cache_entry)
        if cache_entry:
            cache_entry = cache_entry
        pipeline_data[data_defs.CACHE_ENTRY] = cache_entry
        return pipeline_data
