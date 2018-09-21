__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs

class ParseStackPath(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.DOCKER_STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        return pipeline_data
