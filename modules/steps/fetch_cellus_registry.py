__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep

class FetchCellusRegistry(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        return data
  