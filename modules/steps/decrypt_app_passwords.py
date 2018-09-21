__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep

class DecryptAppPasswords(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        return pipeline_data
  