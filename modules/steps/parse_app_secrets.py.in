__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs

class ParseAppSecrets(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.DOCKER_STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        base_dir = os.path.dirname(pipeline_data[data_defs.DOCKER_STACK_FILE_PATH])
        secret_file = os.path.join(base_dir, 'secrets.decrypted.env')
        with open(secret_file, 'r') as file_contents:
            pipeline_data[data_defs.APPLICATION_SECRETS] = file_contents.read()
        return pipeline_data
