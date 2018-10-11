"""RemoveErrorCacheEntry

Removes the (if any) cached error entry created by reporter_service.py
when reporting a raised error during pipline execution"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, redis, environment

class RemoveErrorCacheEntry(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_NAME,
                data_defs.APPLICATION_CLUSTER]

    def run_step(self, pipeline_data):
        client = redis.get_client()
        cluster_name = pipeline_data[data_defs.APPLICATION_CLUSTER]
        application_name = pipeline_data[data_defs.APPLICATION_NAME]
        key = f'{cluster_name}.{application_name}'
        redis.execute_json_delete(client, key)
        return pipeline_data
