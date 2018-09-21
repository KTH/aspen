__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
import modules.util.environment as app_env
import modules.util.data as pipeline_data

class ParseStackFile(BasePipelineStep):

    def get_required_env_variables(self):
        return [app_env.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.DOCKER_STACK_FILE_PATH]

    def run_step(self, data):
        return data
