__author__ = 'tinglev@kth.se'

import yaml
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs

class ParseStackFile(BasePipelineStep):

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [data_defs.DOCKER_STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        file_path = pipeline_data[data_defs.DOCKER_STACK_FILE_PATH]
        with open(file_path, 'r') as content_file:
            pipeline_data[data_defs.STACK_FILE_CONTENTS] = yaml.load(content_file.read())
        return pipeline_data
