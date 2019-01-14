"""ParseStackFile

Reads the deployment docker stack file and parses it to a python object"""

__author__ = 'tinglev@kth.se'

import yaml
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs
from modules.util.exceptions import DeploymentError

class ParseStackFile(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        file_path = pipeline_data[data_defs.STACK_FILE_PATH]
        try:
            with open(file_path, 'r') as content_file:
                raw_data = content_file.read()
                pipeline_data[data_defs.STACK_FILE_RAW_CONTENT] = raw_data
                pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT] = yaml.load(raw_data)
            return pipeline_data
        except yaml.YAMLError:
            raise DeploymentError('Error when parsing docker-stack.yml')
        except FileNotFoundError:
            raise DeploymentError('Error when opening docker-stack.yml')
