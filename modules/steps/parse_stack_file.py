__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs

class ParseStackFile(BasePipelineStep):

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [data_defs.DOCKER_STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        return pipeline_data
