__author__ = 'tinglev@kth.se'

import yaml
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs
from modules.util.exceptions import DeploymentError

class ParseStackFile(BasePipelineStep):

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
        except yaml.YAMLError:
            raise DeploymentError('Error when parsing docker-stack.yml')
        except IOError:
            raise DeploymentError('Error when opening docker-stack.yml')
        return pipeline_data
